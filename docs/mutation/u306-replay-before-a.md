# Mutation table: u306-replay-before-a

Measured by `scripts/mutate.py` on 2026-11-22 14:04 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 234.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 22, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `/home/user/tools/known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u223.M10_report_wrong_name` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 2 | killed |
| `u223.M1_keep_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 3 | killed |
| `u223.M21_discard_through_link` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u223.M22_discard_unlinks_directory` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M23_intent_link_followed` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M24_report_link_followed` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M2_keep_linked_intent` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u223.M4_subdir_unlinked` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u223.M5_discard_keeps_report` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M6_discard_keeps_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 4 | killed |
| `u223.M7_report_any_item` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M8_report_not_mapping` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u223.M9_report_unparsed` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `r395.M9_worker_literal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u192.A3_restamp_wrong_resume` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M11_no_fallback` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u223.M12_renamed_to_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M13_resumed_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M14_any_status` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M15_folder_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M17_claim_failure_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M18_refused_rename_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M19_attempt_start_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u223.M20_twin_target_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R2_extra_not_required` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.R4_keyless_finalized` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R5_tag_write_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R7_absent_energy_stamped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.R8_title_without_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R9_missing_file_analysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.S2_unchanged_rewritten` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.S3_queue_without_calibration` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u90-a.A1_lower_bound_strict` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-a.A2_upper_bound_strict` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-a.A3_range_guard_off` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 7 | killed |
| `u90-a.A4_max_coefficient` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-a.A5_min_coefficient` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-a.A6_dispatch_truthiness` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-a.A7_exclusive_group_gone` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-b.B1_library_root_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-b.B2_method_not_hand` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u90-b.B3_note_reworded` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u90-b.B4_date_field_dropped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-b.B5_previous_cut_not_reported` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-b.B6_hand_detail_drops_old_cut` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 4 | killed |
| `u90-b.B7_fit_detail_drops_old_cut` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-b.B8_hand_reads_old_after_write` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 4 | killed |
| `u90-c.C1_swallow_every_refusal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 22933 | 1 (promoted) | killed |
| `u90-c.C2_unreadable_refuses` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-c.C3_hand_branch_wrong_method` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 4 | killed |
| `u90-d.D1_fit_refuses_over_its_energy_write` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u58-workers-and-wav.E2_uncalibrated_measured` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.E1_beatless_cap` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.S4_undo_overwritten` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.W1_voxlevel_zero` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 4 | killed |
| `u58-workers-and-wav.W2_decoder_seam_ignored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 7 | killed |
| `u58-workers-and-wav.W3_undecodable_scored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.W4_model_guard` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.W5_terminal_decoded` | `src/cratekit/analysis/vocals.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.W7_undecodable_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-zero-row-remeasured.W6_gender_constant` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 172 | 2 | killed |
| `u322.M23_backlog_row_digest_keeps_words` | `src/cratekit/tagging/backlog.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M20_backlog_uses_folder_binder` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M24_backlog_line_gone` | `src/cratekit/tagging/backlog_cli.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M17_deezer_gate_open_always` | `src/cratekit/tagging/published.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M18_deezer_past_an_outage` | `src/cratekit/tagging/published.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M19_suggest_binder_flag_off` | `src/cratekit/tagging/published.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M01_stop_counts_partly_read` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 7 | killed |
| `u322.M02_stop_counts_passed_over` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 5 | killed |
| `u322.M03_partly_read_ignores_passed_over` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M04_partly_read_reads_refusals` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M05_not_sent_read_as_sent` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M06_refused_row_drops_words` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 5 | killed |
| `u322.M07_refusal_words_dropped` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M08_credential_counts` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M09_token_row_asked_every_run` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 1 | killed |
| `u322.M10_old_answer_kept` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 3 | killed |
| `u322.M11_kept_words_lost` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 4 | killed |
| `u322.M12_digest_keeps_words` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M13_beside_any_said_dropped` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M14_token_rows_said_no_token` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 4 | killed |
| `u322.M15_counts_not_sent_as_asked` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M16_counts_stopped_zero` | `src/cratekit/tagging/suggest.py` | user | 6 file(s) | 392 | 2 | killed |
| `u322.M21_suggest_uses_folder_binder` | `src/cratekit/tagging/suggest_cli.py` | user | 6 file(s) | 392 | 1 | killed |
| `u172-b.A14_write_false_trusted` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172-b.A16_tombstone_votes` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A10_tie_not_broken_by_artist` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A11_split_not_written` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A12_fraction_into_weigh` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 2 | killed |
| `u172.A13_report_writes` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A15_read_back_skipped` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A17_bound_read_as_float` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A1_unreadable_read_as_blank` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A2_tagged_file_is_a_candidate` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 7 | killed |
| `u172.A3_off_taxonomy_never_named` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.A5_same_artist_votes_twice` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.A6_vote_per_member` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 5 | killed |
| `u172.A7_playlist_weight_halved` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 6 | killed |
| `u172.A8_artist_weight_halved` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 6 | killed |
| `u172.A9_folder_artist_ignored` | `src/cratekit/tagging/guess.py` | user | 1 file(s) | 119 | 5 | killed |
| `u172.B1_library_read_for_nothing` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B2_unknown_pass_silent` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
| `u172.B3_pass_ignored` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 3 | killed |
| `u172.B4_outcome_ok_always` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 4 | killed |
| `u172.B5_missing_folder_walked` | `src/cratekit/tagging/guess_cli.py` | user | 1 file(s) | 119 | 1 | killed |
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
| `u56-catalogue-searcher-and-tag-workers.R25_digest_drops_the_folder` | `src/cratekit/tagging/retag_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `u292.M01_floor` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M02_proposed_needs_a_write` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 3 | killed |
| `u292.M03_served_needs_a_write` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 3 | killed |
| `u292.M04_file_word_routes_first` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 8 | killed |
| `u292.M05_coarse_never_hides_specific` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 7 | killed |
| `u292.M06_source_names_the_genre_voted` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M07_alias_needs_agreement` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 2 | killed |
| `u292.M08_alias_rows_need_an_entry` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 3 | killed |
| `u292.M09_folder_counts_by_the_row` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 2 | killed |
| `u292.M10_unread_counted` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M11_joining_files_nowhere` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M12_folder_threshold` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M13_neighbours_declared_only` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M14_alias_moving_nothing` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 1 | killed |
| `u292.M15_settled_rows_reached` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1059 | 2 | killed |
| `u292.M16_outcome_over_unread` | `src/cratekit/tagging/backlog_cli.py` | user | 2 file(s) | 1059 | 1 | killed |
| `r799-b.P1_a_file_is_planned_only_while_it_carries_what_a_record_wrote` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-b.P2_two_explanations_are_ambiguous` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P3_a_shops_genre_is_the_shops` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-b.P4_a_rewrite_retires_the_record_it_replaced` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-b.P5_only_a_file_under_the_library_is_opened` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-b.P6_one_file_is_one_group` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r799-b.W2_the_writers_answer_is_kept` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 3 | killed |
| `r799-c.P11_blank_is_not_agreement` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 1 | killed |
| `r799-c.V3_an_unrecorded_rewrite_is_not_clean` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 2 | killed |
| `r799-c.W4_a_rewrite_is_recorded` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 5 | killed |
| `r799-c.W5_a_rewrites_record_is_one_generation_on` | `src/cratekit/tagging/remap.py` | user | 1 file(s) | 93 | 4 | killed |
| `r799-c.V1_the_gate_is_asked_before_the_write` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 15 | killed |
| `r799-c.V2_a_file_that_did_not_take_refuses` | `src/cratekit/tagging/remap_cli.py` | user | 1 file(s) | 93 | 7 | killed |
| `u281.R1_stop_after_four` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 11 | killed |
| `u281.R2_limit_two` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 12 | killed |
| `u281.R3_stopped_reads_miss` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 8 | killed |
| `u281.R4_stopped_note_unmarked` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 3 | killed |
| `u281.R5_no_reset` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 3 | killed |
| `u281.R6_outage_keeps_the_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 1 | killed |
| `u281.R7_one_count_for_every_catalogue` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 3 | killed |
| `u281.W2_searcher_ignores_the_handed_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 10 | killed |
| `u281.W4_binder_drops_the_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 1 | killed |
| `u281.W5_run_never_changes` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 4 | killed |
| `u284.S1_sweep_keeps_no_record` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 4 | killed |
| `u284.S2_outage_sets_a_date` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 1 | killed |
| `u284.S3_answer_never_clears` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 1 | killed |
| `u284.S4_record_kept_without_flag` | `src/cratekit/tagging/searchers.py` | maintainer | 6 file(s) | 374 | 2 | killed |
| `u284.S5_refusal_said_as_outage` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 5 | killed |
| `u284.S6_partial_refusal_said_as_refusal` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 1 | killed |
| `u284.S7_token_step_dropped` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 1 | killed |
| `u284.S8_refusal_not_retryable` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 2 | killed |
| `u284.S9_rejected_token_names_any_shop` | `src/cratekit/tagging/searchers.py` | user | 6 file(s) | 374 | 1 | killed |
| `u171.Z3_floor_lowered` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 26 | 2 | killed |
| `u171.Z4_floor_nudged` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 26 | 1 | killed |
| `u171.Z5_floor_raised` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 26 | 2 | killed |
| `u171.Z6_floor_strict` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 26 | 1 | killed |
| `u171.Z7_any_for_mean` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 26 | 6 | killed |
| `u171.Z1_round_to_ceil` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 26 | 3 | killed |
| `u171.Z2_round_to_truncate` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 26 | 2 | killed |
| `u171.Z8_silence_is_undecodable` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 26 | 1 | killed |
| `u284-composite.C3x_unread_discogs_and_outage_named` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C1_tagged_file_named_refused` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C2_outage_named_refused` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C4_stop_never_collected` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 2 | killed |
| `u284.C5_sweep_stop_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u284.C6_token_unsaid` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 3 | killed |
| `u284.C7_rejected_token_told_to_wait` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 227 | 1 | killed |
| `u281.S5_title_not_named_cloudflare` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 206 | 1 | killed |
| `u281.S6_every_title_named_cloudflare` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 206 | 2 | killed |
| `u281.S7_body_note_reworded` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 206 | 1 | killed |
| `u281.S8_refusal_check_before_the_payload` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 206 | 1 | killed |
| `r1184.M19_tag_folder_wiring` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r1184.M20_tag_folder_fallback` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `r1184.M21_guess_wiring` | `src/cratekit/tagging/guess_cli.py` | user | 3 file(s) | 292 | 1 | killed |
| `u241.M27_no_warm_up_before_the_first_head` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 14 | 1 | killed |
| `u241.M26_warm_up_takes_no_lock` | `src/cratekit/analysis/warm.py` | user | 1 file(s) | 14 | 1 | killed |
| `u281.C1_refusal_said_as_blocked` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 5 | killed |
| `u281.W7_worker_run_key_without_attempt` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 1 | killed |
| `u281.S1_beatport_reads_no_refusal` | `src/cratekit/tagging/searchers.py` | user | 5 file(s) | 440 | 22 | killed |
| `u281.S2_challenge_header_unread` | `src/cratekit/tagging/searchers.py` | user | 5 file(s) | 440 | 3 | killed |
| `u223.M3_no_clear` | `src/cratekit/analysis/artifacts.py` | user | 2 file(s) | 274 | 3 | killed |
| `u157.A2_cut_unbound` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 277 | 3 | killed |
| `r1255.C1_check_landed_unlisted` | `src/cratekit/analysis/rekordbox_check.py` | user | 2 file(s) | 91 | 1 | killed |
| `u181.V1_unavailable_ignores_bound_loader` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 522 | 5 | killed |
| `u244.M23_published_waits_for_discogs` | `src/cratekit/tagging/published.py` | user | 3 file(s) | 336 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R26_retag_queues_no_items` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 122 | 20 | killed |
| `u244.M20_discogs_named_only` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 161 | 1 | killed |

## Zero rows and what they owe

- `u90-d.D1_fit_refuses_over_its_energy_write` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r799-b.P6_one_file_is_one_group` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u223.M10_report_wrong_name`

staged_report: read the report under a name staged_path never writes

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M10_report_wrong_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
```

New text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / f"{item.ordinal}.json"
```

### `u223.M1_keep_intent`

staged_path: clear the rename intent with everything else, the shipped behaviour

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M1_keep_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`

Old text:

```
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
```

New text:

```
                entry.name == "never-kept.json"
                and entry.is_file()
```

### `u223.M21_discard_through_link`

discard_rename_evidence: reach through a linked staging directory

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M21_discard_through_link`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_discard_never_reaches_through_a_linked_staging_directory`

Old text:

```
    if directory.is_symlink() or not directory.is_dir():
        # NOT THROUGH A LINK
```

New text:

```
    if not directory.exists():
        # NOT THROUGH A LINK
```

### `u223.M22_discard_unlinks_directory`

discard_rename_evidence: unlink a directory at the report name, failing the item for good

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M22_discard_unlinks_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`

Old text:

```
        if entry.is_symlink() or not entry.is_dir():
            entry.unlink(missing_ok=True)
```

New text:

```
        if True:
            entry.unlink(missing_ok=True)
```

### `u223.M23_intent_link_followed`

rename_intent: read an intent that is a link

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M23_intent_link_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_or_report_is_never_read_as_the_twin`

Old text:

```
    path = intent_path(cfg, job.job_id, item.ordinal)
    if path.is_symlink() or not path.is_file():
```

New text:

```
    path = intent_path(cfg, job.job_id, item.ordinal)
    if not path.is_file():
```

### `u223.M24_report_link_followed`

staged_report: read a report that is a link

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M24_report_link_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_or_report_is_never_read_as_the_twin`

Old text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
    if path.is_symlink() or not path.is_file():
        return None
```

New text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
    if not path.is_file():
        return None
```

### `u223.M2_keep_linked_intent`

staged_path: keep an intent that is a link, so the clear keeps it and rename_intent follows it

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M2_keep_linked_intent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_is_cleared_rather_than_kept_and_followed`

Old text:

```
                and entry.is_file()
                and not entry.is_symlink()
            ):
```

New text:

```
                and entry.is_file()
            ):
```

### `u223.M4_subdir_unlinked`

staged_path: unlink a subdirectory entry instead of removing its tree

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M4_subdir_unlinked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
```

New text:

```
            if False:
                shutil.rmtree(entry)
```

### `u223.M5_discard_keeps_report`

discard_rename_evidence: drop the intent only, round one's residual

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M5_discard_keeps_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (RENAME_INTENT_FILENAME,):
```

### `u223.M6_discard_keeps_intent`

discard_rename_evidence: drop the report only, keeping the intent

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M6_discard_keeps_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_leaves_no_intent_behind`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (_report_name(item.ordinal),):
```

### `u223.M7_report_any_item`

staged_report: accept a report for another item

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M7_report_any_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    if not isinstance(loaded, dict):
        return None
    return loaded
```

### `u223.M8_report_not_mapping`

staged_report: drop the mapping check, so a list report raises

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M8_report_not_mapping`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    if loaded.get("item") != item.item_id:
        return None
    return loaded
```

### `u223.M9_report_unparsed`

staged_report: let a report that is not JSON raise

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M9_report_unparsed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin`

Old text:

```
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    except OSError:
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

### `r395.M9_worker_literal`

Put the old bare pip literal back in the analysis worker refusal

- File: `src/cratekit/analysis/cli.py`
- Source: `r395.json`, row `M9_worker_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
"install": extras.install_command("analysis")
```

New text:

```
"install": "pip install 'cratekit[analysis]'"
```

### `u192.A3_restamp_wrong_resume`

analyze_restamp: name the analyze run command as the one that resumes an interrupted restamp

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A3_restamp_wrong_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    return _settle(ctx, cfg, job, restamp_argv(job))
```

New text:

```
    return _settle(ctx, cfg, job, analyze_argv(job))
```

### `u223.M11_no_fallback`

_finalized_twin: no staged report fallback when the intent is gone

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M11_no_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if target is None:
        target = _staged_twin(cfg, job, item)
```

New text:

```
(empty)
```

### `u223.M12_renamed_to_unchecked`

_staged_twin: accept an analysed report whatever its renamed_to says

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M12_renamed_to_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
        if report.get("renamed_to") != target.name:
            return None
```

New text:

```
        pass
```

### `u223.M13_resumed_unchecked`

_staged_twin: accept any prefixed skip, not only a resume's

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M13_resumed_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    elif status != "skipped-prefixed" or report.get("resumed_after_rename") is not True:
```

New text:

```
    elif status != "skipped-prefixed":
```

### `u223.M14_any_status`

_staged_twin: accept a report of any status

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M14_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    elif status != "skipped-prefixed" or report.get("resumed_after_rename") is not True:
        return None
```

New text:

```
    elif False:
        return None
```

### `u223.M15_folder_unchecked`

_staged_twin: accept a path outside the item's own folder

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M15_folder_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if target.parent != source.parent:
        return None
    return target
```

New text:

```
    return target
```

### `u223.M17_claim_failure_keeps_evidence`

_finalize: keep the intent when the target name is taken

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M17_claim_failure_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_leaves_no_intent_behind`

Old text:

```
        # read that unrelated file as this item's twin (U223).
        artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
        # read that unrelated file as this item's twin (U223).
```

### `u223.M18_refused_rename_keeps_evidence`

_finalize: keep the intent when the rename is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M18_refused_rename_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`

Old text:

```
        target.unlink(missing_ok=True)
        artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
        target.unlink(missing_ok=True)
```

### `u223.M19_attempt_start_keeps_evidence`

handle_run: keep stale evidence when the source is still a file

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M19_attempt_start_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`

Old text:

```
    # it renames (U223).
    artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
    # it renames (U223).
```

### `u223.M20_twin_target_unchecked`

_finalized_twin: an existing guard, accept a target that is not a file

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M20_twin_target_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_rename_intent_for_another_item_or_a_gone_target_is_not_a_twin`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if target is None or not target.is_file():
        return None
    return target
```

New text:

```
    if target is None:
        return None
    return target
```

### `u58-workers-and-wav.R2_extra_not_required`

Drop the missing extra refusal in the run worker

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R2_extra_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
    _require_heavy(_fake_detect_bound(), "analysing a track")

```

New text:

```
(empty)
```

### `u58-workers-and-wav.R4_keyless_finalized`

Finalize a track whose head found no key

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R4_keyless_finalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_an_undecodable_file_is_its_own_terminal_and_not_a_keyless_track`

Old text:

```
    if partial.get("terminal") is not None:
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": partial["terminal"]}
        )

```

New text:

```
(empty)
```

### `u58-workers-and-wav.R5_tag_write_unchecked`

Ignore a failed tag write and rename anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R5_tag_write_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`

Old text:

```
    _write_or_refuse(path, fields, untouched="The file is untouched and was not renamed")
```

New text:

```
    tags.write_tags(path, fields)
```

### `u58-workers-and-wav.R7_absent_energy_stamped`

Write a level for an absent energy

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R7_absent_energy_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`

Old text:

```
        "energylevel": scored.get("energy"),
```

New text:

```
        "energylevel": scored.get("energy") or 5,
```

### `u58-workers-and-wav.R8_title_without_head`

Write the bare stem as the title tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R8_title_without_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
        "title": rendered.title_tag,
```

New text:

```
        "title": path.stem,
```

### `u58-workers-and-wav.R9_missing_file_analysed`

Drop the source-missing refusal for a file that vanished

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R9_missing_file_analysed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`

Old text:

```
        if twin is None:
            raise _refuse_missing(item, folder, path, "analyse")

```

New text:

```
(empty)
```

### `u58-workers-and-wav.S2_unchanged_rewritten`

Rewrite a file whose level did not move

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S2_unchanged_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`

Old text:

```
    if previous != level:
```

New text:

```
    if True:
```

### `u58-workers-and-wav.S3_queue_without_calibration`

Queue a restamp over a library that has no calibration

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S3_queue_without_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_restamp_with_no_calibration_refuses_at_the_queue`
  - `tests/test_analysis_workers.py::test_the_restamp_refusal_names_the_library_wide_calibrate`

Old text:

```
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    _calibration_or_refuse(cfg)

```

New text:

```
(empty)
```

### `u90-a.A1_lower_bound_strict`

The range guard's lower bound made strict, so a cut of 0 is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A1_lower_bound_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if not VOCAL_SCORE_MIN < cut <= VOCAL_SCORE_MAX:
```

### `u90-a.A2_upper_bound_strict`

The range guard's upper bound made strict, so a cut of 100 is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A2_upper_bound_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if not VOCAL_SCORE_MIN <= cut < VOCAL_SCORE_MAX:
```

### `u90-a.A3_range_guard_off`

The whole range guard switched off, so any float is written as the cut

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A3_range_guard_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[nan]`
  - `tests/test_analysis_workers.py::test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if False:
```

### `u90-a.A4_max_coefficient`

The score range's top moved from 100 to 1000

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A4_max_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte`

Old text:

```
VOCAL_SCORE_MAX = 100.0
```

New text:

```
VOCAL_SCORE_MAX = 1000.0
```

### `u90-a.A5_min_coefficient`

The score range's bottom moved from 0 to minus 1

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A5_min_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`

Old text:

```
VOCAL_SCORE_MIN = 0.0
```

New text:

```
VOCAL_SCORE_MIN = -1.0
```

### `u90-a.A6_dispatch_truthiness`

The hand path dispatched on truthiness, so a cut of 0 falls through to the fit

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A6_dispatch_truthiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`

Old text:

```
    if ctx.args.vocal_cut is not None:
```

New text:

```
    if ctx.args.vocal_cut:
```

### `u90-a.A7_exclusive_group_gone`

The folder and the flag no longer mutually exclusive in the parser

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A7_exclusive_group_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_and_a_hand_cut_together_are_refused_by_the_parser`

Old text:

```
    chosen = parser.add_mutually_exclusive_group()
```

New text:

```
    chosen = parser
```

### `u90-b.B1_library_root_unchecked`

The hand path stops requiring the library root before it writes

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B1_library_root_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_refuses_with_the_library_away`

Old text:

```
    _require_library_root(cfg)
    previous, before = _previous_vocal_cut(cfg)
```

New text:

```
    previous, before = _previous_vocal_cut(cfg)
```

### `u90-b.B2_method_not_hand`

A hand cut recorded under the fit's method, otsu

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B2_method_not_hand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`

Old text:

```
method=VOCAL_METHOD_HAND, note=
```

New text:

```
method="otsu", note=
```

### `u90-b.B3_note_reworded`

The hand cut's note stops saying set by hand

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B3_note_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`

Old text:

```
note=f"set by hand on {today}"
```

New text:

```
note=f"entered on {today}"
```

### `u90-b.B4_date_field_dropped`

The hand cut's set_on date field no longer written

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B4_date_field_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`

Old text:

```
note=f"set by hand on {today}", set_on=today
```

New text:

```
note=f"set by hand on {today}"
```

### `u90-b.B5_previous_cut_not_reported`

The summary reports no previous cut whatever was on record

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B5_previous_cut_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
"previous_vocal_cut": previous}
```

New text:

```
"previous_vocal_cut": None}
```

### `u90-b.B6_hand_detail_drops_old_cut`

The hand path's check detail stops naming the cut it replaced

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B6_hand_detail_drops_old_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
f"cut set by hand at {cut:g}, written to {target}; {before}; "
```

New text:

```
f"cut set by hand at {cut:g}, written to {target}; "
```

### `u90-b.B7_fit_detail_drops_old_cut`

The fit's check detail stops naming the cut it replaced

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B7_fit_detail_drops_old_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`

Old text:

```
        f"written to {target}; {before}",
```

New text:

```
        f"written to {target}",
```

### `u90-b.B8_hand_reads_old_after_write`

The hand path reads the previous cut after its own write, so it reports itself

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B8_hand_reads_old_after_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    previous, before = _previous_vocal_cut(cfg)
    today = _today()
    target = _write_vocal_calibration(
        cfg, cut, method=VOCAL_METHOD_HAND, note=f"set by hand on {today}", set_on=today
    )
```

New text:

```
    today = _today()
    target = _write_vocal_calibration(
        cfg, cut, method=VOCAL_METHOD_HAND, note=f"set by hand on {today}", set_on=today
    )
    previous, before = _previous_vocal_cut(cfg)
```

### `u90-c.C1_swallow_every_refusal`

The previous cut reader swallows every refusal, the permission one included

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-c.json`, row `C1_swallow_every_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        if exc.cause.reason != "vocal-calibration-unreadable":
            raise

```

New text:

```
(empty)
```

### `u90-c.C2_unreadable_refuses`

An unreadable calibration refuses the hand cut instead of being replaced by it

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-c.json`, row `C2_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`

Old text:

```
        return None, "the calibration on record before could not be read, and this replaces it"
```

New text:

```
        raise
```

### `u90-c.C3_hand_branch_wrong_method`

The replaced cut is named as set by hand only when its method is otsu

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-c.json`, row `C3_hand_branch_wrong_method`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    if record.get("method") == VOCAL_METHOD_HAND:
```

New text:

```
    if record.get("method") == "otsu":
```

### `u90-d.D1_fit_refuses_over_its_energy_write`

The fit lets a refusal from the previous cut read escape after the energy calibration is written

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-d.json`, row `D1_fit_refuses_over_its_energy_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        _, before = _previous_vocal_cut(cfg)
    except CratekitError as exc:
```

New text:

```
    _, before = _previous_vocal_cut(cfg)
    if False:
        exc = None
```

### `u58-workers-and-wav.E2_uncalibrated_measured`

Measure energy with no calibration instead of reporting uncalibrated

- File: `src/cratekit/analysis/detect.py`
- Source: `u58-workers-and-wav.json`, row `E2_uncalibrated_measured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_detector_names_why_energy_is_what_it_is`

Old text:

```
    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED

```

New text:

```
(empty)
```

### `u58-workers-and-wav.E1_beatless_cap`

Drop the beatless cap in the energy scorer

- File: `src/cratekit/analysis/energy.py`
- Source: `u58-workers-and-wav.json`, row `E1_beatless_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_beatless_guard_caps_a_loud_track_with_no_onsets`

Old text:

```
    if calibration.onset_floor is not None:
        density = float(features.get("onset_density", math.inf))
        if not math.isnan(density) and density < calibration.onset_floor:
            level = min(level, BEATLESS_CAP)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.S4_undo_overwritten`

Let a second restamp overwrite the first previous value

- File: `src/cratekit/analysis/energy.py`
- Source: `u58-workers-and-wav.json`, row `S4_undo_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_undo_log_keeps_the_first_previous_value_across_a_second_restamp`

Old text:

```
        if key in log:
            return False

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W1_voxlevel_zero`

The original defect: score every track voxlevel 0 with a model loaded

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W1_voxlevel_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = 0
```

### `u58-workers-and-wav.W2_decoder_seam_ignored`

Ignore the bound decoder and always use the shipped one

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W2_decoder_seam_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_run_with_the_model_loaded_carries_no_vocal_warning`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    decoder = _DECODER
    if decoder is None:
        from cratekit.analysis.vocal import decode

        decoder = decode
    return decoder(path)
```

New text:

```
    from cratekit.analysis.vocal import decode

    return decode(path)
```

### `u58-workers-and-wav.W3_undecodable_scored`

Drop the guard that reports a failed decode instead of scoring it

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W3_undecodable_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`

Old text:

```
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W4_model_guard`

Drop the guard for a model that did not load

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W4_model_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`

Old text:

```
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W5_terminal_decoded`

Decode a track whose head was terminal anyway

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W5_terminal_decoded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_terminal_head_is_not_decoded_at_all`

Old text:

```
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W7_undecodable_reason_reworded`

Reword the undecodable reason, do not append

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W7_undecodable_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`

Old text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-undecodable"
```

New text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-unreadable"
```

### `u58-zero-row-remeasured.W6_gender_constant`

Report every scored track's gender as U

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-zero-row-remeasured.json`, row `W6_gender_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
    result["voxgender"] = score.gender
```

New text:

```
    result["voxgender"] = "U"
```

### `u322.M23_backlog_row_digest_keeps_words`

backlog.Row.digested: the backlog digest keeps the words

- File: `src/cratekit/tagging/backlog.py`
- Source: `u322.json`, row `M23_backlog_row_digest_keeps_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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

### `u322.M20_backlog_uses_folder_binder`

backlog_cli.read_plan: the backlog asks through tag folder's binder, so Deezer is held behind a refusing Beatport

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u322.json`, row `M20_backlog_uses_folder_binder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_refusing_beatport_beside_an_answering_discogs_asks_every_row_and_counts_them`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
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

### `u322.M17_deezer_gate_open_always`

second_opinion: the flag is ignored, so tag folder asks Deezer past a refusing Beatport too

- File: `src/cratekit/tagging/published.py`
- Source: `u322.json`, row `M17_deezer_gate_open_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[refused]`
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
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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

### `u322.M03_partly_read_ignores_passed_over`

Asked.partly_read: a passed over row reads as partly read, so it resets a run of refusals

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M03_partly_read_ignores_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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

### `u322.M07_refusal_words_dropped`

catalogue_lookup: a refusal raised by the searcher carries no words, so the line counts its catalogues not asked

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M07_refusal_words_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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

### `u322.M09_token_row_asked_every_run`

KeptCatalogue._askable_now: a row passed over for a refused token is asked again by every run of the day

- File: `src/cratekit/tagging/suggest.py`
- Source: `u322.json`, row `M09_token_row_asked_every_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
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

### `u322.M21_suggest_uses_folder_binder`

suggest_cli.read_plan: tag suggest asks through tag folder's binder

- File: `src/cratekit/tagging/suggest_cli.py`
- Source: `u322.json`, row `M21_suggest_uses_folder_binder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_suggest.py::test_tag_suggest_asks_deezer_past_a_refusing_beatport_by_each_files_isrc`

Old text:

```
            searchers.for_taxonomy(declared), published.for_suggestions(declared)
```

New text:

```
            searchers.for_taxonomy(declared), published.for_taxonomy(declared)
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

### `u172.A1_unreadable_read_as_blank`

plan: drop the unreadable branch, so a file whose genre could not be read is a candidate and written over

- File: `src/cratekit/tagging/guess.py`
- Source: `u172.json`, row `A1_unreadable_read_as_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_file_whose_genre_could_not_be_read_is_not_a_blank`

Old text:

```
        if not one.readable:
```

New text:

```
        if False:
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

### `u172.B5_missing_folder_walked`

tag_guess: drop the refusal of a folder that is not there

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `u172.json`, row `B5_missing_folder_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_a_folder_that_is_not_there_refuses`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if False:
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

### `u292.M01_floor`

FLOOR: propose at medium rather than high

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M01_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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

### `u292.M06_source_names_the_genre_voted`

proposal_of: a catalogue match for another genre is named the source

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M06_source_names_the_genre_voted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_proposal_the_library_alone_voted_for_names_the_neighbours`

Old text:

```
        and asked.genre == item.genre

```

New text:

```
        and True

```

### `u292.M07_alias_needs_agreement`

word_of: an alias offered at any band, low included

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M07_alias_needs_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_word_one_short_of_the_threshold_with_no_agreement_is_left_first`
  - `tests/test_tag_backlog.py::test_neighbours_agreeing_only_at_low_do_not_recommend_an_alias`

Old text:

```
        if band in _NEIGHBOURS_AGREE

```

New text:

```
        if band != suggest.NONE

```

### `u292.M08_alias_rows_need_an_entry`

word_of: an alias's rows follow with no genre entry for its genre

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M08_alias_rows_need_an_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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
- Collected: 1059 against a baseline of 1059
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

### `u292.M12_folder_threshold`

word_of: the folder recommended one row above the threshold

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M12_folder_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_folder_that_would_file_the_threshold_is_recommended_first`

Old text:

```
    if folder is not None and folder.rows >= genres_report.FOLDER_WORTH:
```

New text:

```
    if folder is not None and folder.rows > genres_report.FOLDER_WORTH:
```

### `u292.M13_neighbours_declared_only`

neighbour_votes: a neighbour carrying an undeclared word votes

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M13_neighbours_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_a_neighbour_votes_once_for_a_whole_word_at_its_higher_weight`

Old text:

```
        if other.content_id in ids or not suggest.suggestable(declared, other.genre):
```

New text:

```
        if other.content_id in ids:
```

### `u292.M14_alias_moving_nothing`

word_of: an alias moving no row recommended, round two's finding

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M14_alias_moving_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_backlog.py::test_an_alias_to_a_genre_the_library_has_no_entry_for_moves_nothing`

Old text:

```
    elif alias is not None and alias.rows:
```

New text:

```
    elif alias is not None:
```

### `u292.M15_settled_rows_reached`

plan_backlog: every row of a settled word read as settled, reached or not

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M15_settled_rows_reached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
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

### `u292.M16_outcome_over_unread`

the verb: a backlog of unread rows alone ends no_op, round one's clean report

- File: `src/cratekit/tagging/backlog_cli.py`
- Source: `u292.json`, row `M16_outcome_over_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
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
- Collected: 22933 against a baseline of 22933
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

### `u281.R1_stop_after_four`

Refusals.stopped: stop only once the count passes the limit, so four refusals are sent, not three

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R1_stop_after_four`
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

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R2_limit_two`
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

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R3_stopped_reads_miss`
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

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R4_stopped_note_unmarked`
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

### `u281.R5_no_reset`

Refusals.heard: an answer that is not a refusal never ends the run of them, so a catalogue that answered can be stopped

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R5_no_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_match_resets_the_count_as_a_miss_does`
  - `tests/test_beatport_refusal.py::test_an_outage_between_refusals_ends_the_run_of_them`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`

Old text:

```
        else:
            self.running.pop(outcome.source, None)
            self.last.pop(outcome.source, None)
```

New text:

```
        else:
            pass
```

### `u281.R6_outage_keeps_the_count`

Refusals.heard: only a match or a miss resets, so refused, refused, down, refused stops the run

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R6_outage_keeps_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_an_outage_between_refusals_ends_the_run_of_them`

Old text:

```
        else:
            self.running.pop(outcome.source, None)
```

New text:

```
        elif outcome.answer in (Answer.MISS, Answer.MATCHED):
            self.running.pop(outcome.source, None)
```

### `u281.R7_one_count_for_every_catalogue`

Refusals.heard: count every catalogue's refusals under one key, so a refusing fallback stops Beatport too

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `R7_one_count_for_every_catalogue`
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

### `u281.W4_binder_drops_the_count`

for_taxonomy: hand the searcher no count, so the worker's run count never reaches it

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W4_binder_drops_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`

Old text:

```
    return catalogue_searcher(declared, discogs=for_discogs(), refusals=refusals)
```

New text:

```
    return catalogue_searcher(declared, discogs=for_discogs(), refusals=None)
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

### `u284.S1_sweep_keeps_no_record`

searchers.for_run: the sweep's run count keeps no record, so no date is ever known

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S1_sweep_keeps_no_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
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

### `u284.S2_outage_sets_a_date`

Refusals.heard: an outage is recorded as a refusal, giving a false refusing since date

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S2_outage_sets_a_date`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_an_outage_never_sets_a_refusal_date`

Old text:

```
        if outcome.answer is Answer.BLOCKED:
            refused.refused(outcome.source)
```

New text:

```
        if outcome.answer in (Answer.BLOCKED, Answer.UNREACHABLE):
            refused.refused(outcome.source)
```

### `u284.S3_answer_never_clears`

Refusals.heard: a match or a miss never clears the record

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S3_answer_never_clears`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_miss_from_the_refusing_catalogue_clears_it_and_an_outage_does_not`

Old text:

```
            refused.answered(outcome.source)
```

New text:

```
            pass
```

### `u284.S4_record_kept_without_flag`

Refusals.heard: every run count keeps the record, a searcher built by any caller included

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S4_record_kept_without_flag`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_refusal_with_no_date_recorded_still_names_the_catalogue`
  - `tests/test_sync_refused.py::test_a_searcher_built_with_no_run_count_keeps_no_record`

Old text:

```
        if not self.record:
            return

```

New text:

```
(empty)
```

### `u284.S5_refusal_said_as_outage`

searchers._decide: a refusal by every catalogue raises the outage refusal, network step first and no token step

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S5_refusal_said_as_outage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
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

### `u284.S6_partial_refusal_said_as_refusal`

searchers._decide: a refusal beside an outage is said as a refusal by all, hiding the outage

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S6_partial_refusal_said_as_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_a_refusal_beside_an_outage_is_an_outage_first`

Old text:

```
    if len(blocked) == len(outcomes):
        raise _refused_by_all
```

New text:

```
    if blocked:
        raise _refused_by_all
```

### `u284.S7_token_step_dropped`

searchers._refused_by_all: no token step when Discogs went unasked

- File: `src/cratekit/tagging/searchers.py`
- Source: `u284.json`, row `S7_token_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_beatport_refusal.py`, `tests/test_discogs_searcher.py`, `tests/test_discogs_first.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 374 against a baseline of 374
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
- Collected: 374 against a baseline of 374
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
- Collected: 374 against a baseline of 374
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

### `u171.Z3_floor_lowered`

vocal.DEFAULT_FRAME_FLOOR: 0.05 to 0.03, so a lead the model hears at 0.034 scores

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z3_floor_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_lead_the_model_never_hears_at_the_floor_scores_zero`
  - `tests/test_vocal_zeros.py::test_the_floor_is_reached_at_exactly_its_value_and_not_just_under`

Old text:

```
DEFAULT_FRAME_FLOOR = 0.05
```

New text:

```
DEFAULT_FRAME_FLOOR = 0.03
```

### `u171.Z4_floor_nudged`

vocal.DEFAULT_FRAME_FLOOR: 0.05 to 0.045, a realistic nearby value the review found unpinned

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z4_floor_nudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_the_floor_is_reached_at_exactly_its_value_and_not_just_under`

Old text:

```
DEFAULT_FRAME_FLOOR = 0.05
```

New text:

```
DEFAULT_FRAME_FLOOR = 0.045
```

### `u171.Z5_floor_raised`

vocal.DEFAULT_FRAME_FLOOR: 0.05 to 0.10, so a trace heard at 0.08 never counts

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z5_floor_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.006-1]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.014-1]`

Old text:

```
DEFAULT_FRAME_FLOOR = 0.05
```

New text:

```
DEFAULT_FRAME_FLOOR = 0.10
```

### `u171.Z6_floor_strict`

vocal.presence_score: a frame at exactly the floor no longer counts

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z6_floor_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_the_floor_is_reached_at_exactly_its_value_and_not_just_under`

Old text:

```
    return 100.0 * float((series >= frame_floor).mean())
```

New text:

```
    return 100.0 * float((series > frame_floor).mean())
```

### `u171.Z7_any_for_mean`

vocal.presence_score: any frame at the floor scores 100, so coverage becomes presence

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z7_any_for_mean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_sung_lead_shaped_like_a64s_known_vocals_scores_above_the_cut`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.0008-0]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.0049-0]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.006-1]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.014-1]`
  - `tests/test_vocal_zeros.py::test_the_stamp_is_the_share_of_frames_at_the_floor_rounded`

Old text:

```
    return 100.0 * float((series >= frame_floor).mean())
```

New text:

```
    return 100.0 * float((series >= frame_floor).any())
```

### `u171.Z1_round_to_ceil`

vocals.analyse: stamp a trace under half a percent as 1 by rounding the presence up

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z1_round_to_ceil`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.0008-0]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.0049-0]`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.014-1]`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = int(-(-score.presence // 1))
```

### `u171.Z2_round_to_truncate`

vocals.analyse: truncate the presence instead of rounding, so 0.6 percent stamps 0

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z2_round_to_truncate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_a_sung_lead_shaped_like_a64s_known_vocals_scores_above_the_cut`
  - `tests/test_vocal_zeros.py::test_a_trace_under_half_a_percent_of_frames_rounds_to_zero[0.006-1]`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = int(score.presence)
```

### `u171.Z8_silence_is_undecodable`

vocal.decode seam in vocals.analyse: a silent decode reported as undecodable rather than heard as 0

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z8_silence_is_undecodable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocal_zeros.py::test_silence_is_heard_and_scores_zero_rather_than_no_score`

Old text:

```
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)
```

New text:

```
    if samples is None or not samples.any():
        return _inactive(result, REASON_AUDIO_UNDECODABLE)
```

### `u284-composite.C3x_unread_discogs_and_outage_named`

tagging.cli._refused_out: the composite for C3's zero, both the Discogs was read guard and the every other catalogue refused guard removed, so any file left with no genre is named as one the catalogues refused

- File: `src/cratekit/tagging/cli.py`
- Source: `u284-composite.json`, row `C3x_unread_discogs_and_outage_named`
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

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C1_tagged_file_named_refused`
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

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C2_outage_named_refused`
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

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C4_stop_never_collected`
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

### `u284.C6_token_unsaid`

tagging.cli._refusal_stop: Discogs unasked is never said and its token step never given

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C6_token_unsaid`
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

- File: `src/cratekit/tagging/cli.py`
- Source: `u284.json`, row `C7_rejected_token_told_to_wait`
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

### `u281.S5_title_not_named_cloudflare`

unread_outcome: never name a Cloudflare title page a Cloudflare challenge

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S5_title_not_named_cloudflare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_just_a_moment_page_is_blocked_not_a_parse_break`

Old text:

```
        named = f", a {CLOUDFLARE_CHALLENGE}" if _CLOUDFLARE_TITLE.match(title) else ""
```

New text:

```
        named = ""
```

### `u281.S6_every_title_named_cloudflare`

unread_outcome: name every challenge title Cloudflare's, Bandcamp's own Client Challenge included

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S6_every_title_named_cloudflare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 206 against a baseline of 206
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

### `u281.S7_body_note_reworded`

unread_outcome: the challenge script's note loses the Cloudflare challenge words the summary counts by

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S7_body_note_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_page_carrying_only_cloudflares_script_is_blocked`

Old text:

```
            note=f"the catalogue answered with a {CLOUDFLARE_CHALLENGE} page",
```

New text:

```
            note="the catalogue answered with Cloudflare's challenge page",
```

### `u281.S8_refusal_check_before_the_payload`

_search_beatport: run the refusal check before the parse again, round one's order, so a results page carrying Cloudflare's script reads as a refusal

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S8_refusal_check_before_the_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 206 against a baseline of 206
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_results_page_carrying_cloudflares_script_is_read_as_results`

Old text:

```
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
```

New text:

```
    refused = unread_outcome(BEATPORT, page)
    if refused is not None:
        return refused
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
```

### `r1184.M19_tag_folder_wiring`

tag folder report: never hand the warning the taxonomy, so the own name answer is dropped

- File: `src/cratekit/tagging/cli.py`
- Source: `r1184.json`, row `M19_tag_folder_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
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
- Collected: 292 against a baseline of 292
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

### `r1184.M21_guess_wiring`

tag guess: drop the own name sentence from the off taxonomy warning

- File: `src/cratekit/tagging/guess_cli.py`
- Source: `r1184.json`, row `M21_guess_wiring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_tag_workers.py`, `tests/test_tag_guess.py`
- Collected: 292 against a baseline of 292
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

### `u241.M27_no_warm_up_before_the_first_head`

analyse_file: no warm up, so two workers on a cold cache compile into it together, crash, and leave it damaged

- File: `src/cratekit/analysis/detect.py`
- Source: `u241.json`, row `M27_no_warm_up_before_the_first_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_warm.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_warm.py::test_the_detector_asks_for_the_warm_up_before_it_decodes`

Old text:

```
    warm.kernels()

```

New text:

```
    warm.kernels  # not called

```

### `u241.M26_warm_up_takes_no_lock`

warm.exclusive: the lock is opened and never taken, so two processes fill the kernel cache together

- File: `src/cratekit/analysis/warm.py`
- Source: `u241.json`, row `M26_warm_up_takes_no_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_warm.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_warm.py::test_two_processes_are_never_inside_the_lock_together`

Old text:

```
        fcntl.flock(handle, fcntl.LOCK_EX)

```

New text:

```
        pass

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

### `u281.S1_beatport_reads_no_refusal`

_search_beatport: drop the shared refusal check, so a 403 is unreachable and a 200 challenge a parse break, as before the card

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S1_beatport_reads_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`
- Collected: 440 against a baseline of 440
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

### `u281.S2_challenge_header_unread`

_refusal_note: never read Cf-Mitigated, so a Cloudflare 403 is only HTTP 403 and the warning cannot name the challenge

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S2_challenge_header_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`
- Collected: 440 against a baseline of 440
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_403_carrying_cloudflares_challenge_header_is_blocked_and_named`
  - `tests/test_beatport_refusal.py::test_the_challenge_header_is_read_whatever_case_its_name_and_value_arrive_in`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`

Old text:

```
    if mitigated.strip().lower() == _CF_CHALLENGE:
```

New text:

```
    if False:
```

### `u223.M3_no_clear`

staged_path: clear nothing, so a stale report and scratch leak into the next attempt

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M3_no_clear`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_tag_workers.py`
- Collected: 274 against a baseline of 274
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_linked_intent_is_cleared_rather_than_kept_and_followed`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
```

New text:

```
            continue
```

### `u157.A2_cut_unbound`

_bind_defaults: bind no drift cut, so the detector reads the shipped default

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A2_cut_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`, `tests/test_head_agreement.py`
- Collected: 277 against a baseline of 277
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_worker_process_with_nothing_bound_binds_the_shipped_defaults`
  - `tests/test_analysis_workers.py::test_the_default_detector_is_rebound_with_a_fresh_calibration_per_item`
  - `tests/test_drift.py::test_a_whole_number_cut_loads_and_reaches_the_detector_binding`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,

```

New text:

```
(empty)
```

### `r1255.C1_check_landed_unlisted`

_landed: never stop on the listing, so the pass lookup refuses in words of its own

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `r1255.json`, row `C1_check_landed_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_analyze_check.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`

Old text:

```
    if session.log_unlisted(unreadable, cfg):
        # NO LANDING CAN BE READ
```

New text:

```
    if False:
        # NO LANDING CAN BE READ
```

### `u181.V1_unavailable_ignores_bound_loader`

vocals.unavailable: ask missing_requirement even with a loader bound, so a bound fake reads as unable

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V1_unavailable_ignores_bound_loader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_doctor.py`
- Collected: 522 against a baseline of 522
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`
  - `tests/test_sync_land.py::test_the_outbound_hearts_write_stays_behind_its_own_gate`
  - `tests/test_vocals_cli.py::test_the_one_test_takes_a_bound_loader_as_able`

Old text:

```
    return None if loader_bound() else missing_requirement()
```

New text:

```
    return missing_requirement()
```

### `u244.M23_published_waits_for_discogs`

second_opinion: ask the general catalogue while Discogs was asked and unread

- File: `src/cratekit/tagging/published.py`
- Source: `u244.json`, row `M23_published_waits_for_discogs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_published_genre.py`, `tests/test_tag_workers.py`
- Collected: 336 against a baseline of 336
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
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
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

### `u244.M20_discogs_named_only`

_resolved: choose Discogs' style without requiring an exact folder declaration

- File: `src/cratekit/tagging/searchers.py`
- Source: `u244.json`, row `M20_discogs_named_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`
- Collected: 161 against a baseline of 161
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

