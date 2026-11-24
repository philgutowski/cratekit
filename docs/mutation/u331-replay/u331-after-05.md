# Mutation table: u331-after-05

Measured by `scripts/mutate.py` on 2026-11-24 02:09 UTC, branch `HEAD` at `d29860c2`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23132 collected. pytest invocations for this batch: 166.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 02:08 UTC for commit `d29860c2a9b3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 26, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23132 against 23132. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u90-a.A1_lower_bound_strict` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-a.A2_upper_bound_strict` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-a.A3_range_guard_off` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 7 | killed |
| `u90-a.A4_max_coefficient` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 2 | killed |
| `u90-a.A5_min_coefficient` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 2 | killed |
| `u90-a.A6_dispatch_truthiness` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-b.B1_library_root_unchecked` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-b.B2_method_not_hand` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 3 | killed |
| `u90-b.B3_note_reworded` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 3 | killed |
| `u90-b.B4_date_field_dropped` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-b.B5_previous_cut_not_reported` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 2 | killed |
| `u90-b.B6_hand_detail_drops_old_cut` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 4 | killed |
| `u90-b.B7_fit_detail_drops_old_cut` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 2 | killed |
| `u90-b.B8_hand_reads_old_after_write` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 4 | killed |
| `u90-c.C2_unreadable_refuses` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-c.C3_hand_branch_wrong_method` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 4 | killed |
| `u94-a.S1_floor_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 3 | killed |
| `u94-a.S2_floor_off_by_one` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u94-a.S3_partial_refusal_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 6 | killed |
| `u94-a.S4_accept_flag_dead` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 11 | killed |
| `u94-a.S5_recursive_not_required` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u94-a.S6_music_folder_not_wide` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-a.S7_samefile_to_spelling` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-a.S8_after_walk_never_asked` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W1_after_walk_refusal_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W3_accepted_reads_ok` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u94-b.W4_partial_warning_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u94-b.W5_warning_without_a_write` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W6_outcome_energy_only` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W7_omissions_dropped_from_the_fit` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W8_note_forgets_the_omission` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N1_stride_is_the_first_n` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u94-c.N2_stride_is_a_fixed_step` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N3_sample_ignored` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 3 | killed |
| `u94-c.N4_vocal_half_sampled` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N5_note_m_is_the_sample` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N7_root_not_required_first` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N8_absent_folder_not_told_apart` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `r744.E8_record_applies_to_every_window` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 65 | 1 | killed |
| `r744.E9_record_does_not_sum` | `src/cratekit/analysis/detect.py` | maintainer | 1 file(s) | 65 | 1 | killed |
| `u241.M27_no_warm_up_before_the_first_head` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 15 | 1 | killed |
| `u58-workers-and-wav.E2_uncalibrated_measured` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 177 | 1 | killed |
| `r706-c.C1_parts_note_never_said` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `r924.C3_recording_drops_progress` | `src/cratekit/intake/cli_identify.py` | user | 3 file(s) | 119 | 2 | killed |
| `r925.S3_no_write` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 3 | killed |
| `r925.S4_write_failure_refuses` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `r925.S5_unwritten_note_names_no_job_show` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u103-b.C10_open_question_is_pending` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u103-b.C14_offered_under_its_own_key` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u103-b.C3_out_must_be_a_folder` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u103-b.C6_served_note` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u103-b.C7_unwritten_note` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u103-b.C9_refusal_counts_the_gap` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u104-d.C2_refusal_named_for_the_address` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-d.C3_detail_renamed` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-d.C4_scratch_left_said` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-d.C5_no_digest_token_is_the_address` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-e.E2_timeout_is_retryable` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-e.E4_identify_library_before_fetch` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 2 | killed |
| `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u112-b.C7_outcome_always_ok` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.C1_report_asks` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 52 | killed |
| `u112.C5_unexpected_failure_stops` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u112.C6_failure_never_raised` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 3 | killed |
| `u137.C1_named_always` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 17 | killed |
| `u137.C2_only_dropped` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 23 | killed |
| `u137.C3_choices_dropped` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 97 | 1 | killed |
| `u222.M21_cli_message_unchanged` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 255 | 2 | killed |
| `u222.M22_cli_detail_unchanged` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 255 | 1 | killed |
| `u222.M23_cli_empty_stale_reworded` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 255 | 1 | killed |
| `u267.M1_report_shares_nothing` | `src/cratekit/organize/cli.py` | user | 3 file(s) | 149 | 5 | killed |
| `u267.M2_applying_run_shares` | `src/cratekit/organize/cli.py` | user | 2 file(s) | 111 | 1 | killed |
| `u267.M3_report_never_closes` | `src/cratekit/organize/cli.py` | user | 2 file(s) | 111 | 4 | killed |
| `r1184.M19_tag_folder_wiring` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 289 | 1 | killed |
| `r1184.M20_tag_folder_fallback` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 289 | 1 | killed |
| `r1476.M10_no_name_slug_step` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 4 | killed |
| `r1476.M11_slug_step_beats_exact_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M12_no_identifier_fallback` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 3 | killed |
| `r1476.M13_needles_not_held` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 11 | killed |
| `r1476.M14_genre_join_by_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M15_answer_without_genre` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 5 | killed |
| `r1476.M16_unsluggable_raises` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M17_remedy_names_display_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 3 | killed |
| `r1476.M18_remedy_head_never_shared` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M19_outranked_wording` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M1_identifier_not_frozen` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 7 | killed |
| `r1476.M2_folder_seam_by_name` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M3_folder_seam_with_no_identifier` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M6_worker_hands_no_folder_seam` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 2 | killed |
| `r1476.M7_worker_hands_identifier_as_label` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 1 | killed |
| `r1476.M8_shared_name_takes_first` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 10 | killed |
| `r1476.M9_identifier_first` | `src/cratekit/tagging/cli.py` | user | 4 file(s) | 286 | 5 | killed |
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
| `u178.S2_unknown_label_refused` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S3_unreadable_registry_refuses_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S4_genres_frozen` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 13 | killed |
| `u178.S5_worker_takes_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 7 | killed |
| `u178.S6_outranked_needs_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 4 | killed |
| `u192.T1_typed_label_on_queue` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T2_queue_warnings_lost` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T3_resume_label_unsaid` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 2 | killed |
| `u192.T4_tag_queue_only_ignored` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 221 | 7 | killed |
| `u240.M11_needle_is_the_name` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 2 | killed |
| `u240.M12_raw_line_matched` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 2 | killed |
| `u240.M13_two_way_match` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 7 | killed |
| `u240.M14_widest_any` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 1 | killed |
| `u240.M15_no_widest_rule` | `src/cratekit/tagging/cli.py` | user | 5 file(s) | 338 | 1 | killed |
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

## Considered and dropped

Recorded rows this replay left out and did NOT measure. They are not coverage, and `scripts/killset.py check` fails on one that was killed before and is neither a row nor mapped here.

- `u276.K13_record_key_method_dropped`: head_agreement: leave out key_method, so the run's answer no longer says which method its key was read with Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 took the key stage out of the detector and removed `record["key_method"] = KEY_DEFAULT` from head_agreement in analysis/detect.py, with tests/test_analysis_key_default.py deleted; the run reads no key, so its record names no key method
- `u276.K14_record_read_with_plain`: _HEAD_AGREEMENT: say its key buckets were read with plain, which they were not Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed the key bucket from _HEAD_AGREEMENT in analysis/detect.py, `"key": {"equal": 158, "differs": 141},` and `"key_read_with": "whole",` with it
- `u276.K1_default_is_whole`: KEY_DEFAULT: the whole track again, so every caller naming no method separates and the key reverts to the old reading Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed the key methods from analysis/detect.py: `KEY_PLAIN = "plain"`, `KEY_METHODS = (KEY_WHOLE, KEY_WINDOWS, KEY_PLAIN)` and `KEY_DEFAULT = KEY_PLAIN`; no key default exists at the head
- `u276.K2_profile_default_whole`: key_profile: default its method to whole by name, past KEY_DEFAULT, so a caller of the profile alone separates Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed `def key_profile(` from analysis/detect.py, its parameter `    method: str = KEY_DEFAULT,` with it; the detector has no key profile
- `u276.K3_analyse_file_default_whole`: analyse_file: default its key to whole by name, so analyze run and its workers, which name none, separate Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed analyse_file's parameter `    key: str = KEY_DEFAULT,` in analysis/detect.py; analyse_file now returns tempo, drift and energy and takes no key method
- `u276.K5_stages_of_plain_keeps_harmonic`: stages_of: answer every stage for plain too, so the stage report counts a separation the plain chroma never ran Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed `def stages_of(method: str) -> tuple[str, ...]:` and its `if method == KEY_PLAIN:` branch from analysis/detect.py, replacing `STAGES = ("decode", "tempo_drift", "harmonic", "chroma_key", "energy")` with `STAGES = ("decode", "tempo_drift", "energy")`; no method chooses stages at the head
- `u276.K6_stages_of_refuses_nothing`: stages_of: drop the refusal of a method nobody built, so a misspelt method reads as one that separates Dropped because: gone at the head, removed by U343 on main (b1e44ba9), not by U331: U343's b1e44ba9 removed stages_of, its `if method not in KEY_METHODS:` refusal with it, from analysis/detect.py; there is no key method to refuse at the head

## Row definitions

### `u90-a.A1_lower_bound_strict`

The range guard's lower bound made strict, so a cut of 0 is refused

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A1_lower_bound_strict`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A2_upper_bound_strict`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A3_range_guard_off`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A4_max_coefficient`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A5_min_coefficient`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A6_dispatch_truthiness`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

### `u90-b.B1_library_root_unchecked`

The hand path stops requiring the library root before it writes

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B1_library_root_unchecked`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B2_method_not_hand`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B3_note_reworded`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B4_date_field_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B5_previous_cut_not_reported`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B6_hand_detail_drops_old_cut`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B7_fit_detail_drops_old_cut`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B8_hand_reads_old_after_write`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

### `u90-c.C2_unreadable_refuses`

An unreadable calibration refuses the hand cut instead of being replaced by it

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-c.json`, row `C2_unreadable_refuses`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-c.json`, row `C3_hand_branch_wrong_method`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

### `u94-a.S1_floor_dropped`

analyze_calibrate: never refuse a sample below the fit floor, so --sample 3 measures three tracks and fails after the walk instead of before it

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S1_floor_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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

### `u94-b.W6_outcome_energy_only`

analyze_calibrate: derive the outcome from the energy half alone, so a run that replaced only the vocal cut answers no_op

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W6_outcome_energy_only`
- Moved: the calibrate verb's body moved from analysis/cli.py to analysis/calibrate.py, a file the base did not hold, and the text occurs once there
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
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

### `u94-b.W7_omissions_dropped_from_the_fit`

analyze_calibrate: leave the walk's omissions off the envelope of a fit that went ahead

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W7_omissions_dropped_from_the_fit`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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

### `u94-c.N7_root_not_required_first`

analyze_calibrate: ask the folder's standing with the library away, so an unmounted volume is blamed on the folder

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N7_root_not_required_first`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
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
- Collected: 213 against a baseline of 213
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

### `u241.M27_no_warm_up_before_the_first_head`

analyse_file: no warm up, so two workers on a cold cache compile into it together, crash, and leave it damaged

- File: `src/cratekit/analysis/detect.py`
- Source: `u241.json`, row `M27_no_warm_up_before_the_first_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_warm.py`
- Collected: 15 against a baseline of 15
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

### `u58-workers-and-wav.E2_uncalibrated_measured`

Measure energy with no calibration instead of reporting uncalibrated

- File: `src/cratekit/analysis/detect.py`
- Source: `u58-workers-and-wav.json`, row `E2_uncalibrated_measured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
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

### `r706-c.C1_parts_note_never_said`

The recognition-in-parts note is never added

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r706-c.json`, row `C1_parts_note_never_said`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
    if result.parts <= 1:
        return ()
    still = (
```

New text:

```
    if result.parts >= 1:
        return ()
    still = (
```

### `r924.C3_recording_drops_progress`

_recording does not pass its progress to the fetch

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r924.json`, row `C3_recording_drops_progress`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_human_fetch_runs_its_watcher`

Old text:

```
            address, Path(cfg.library.root), found, progress=progress
```

New text:

```
            address, Path(cfg.library.root), found
```

### `r925.S3_no_write`

intake set writes no tracklist and says it wrote one

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r925.json`, row `S3_no_write`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/intake/test_set_fetch.py`
- Collected: 108 against a baseline of 108
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`

Old text:

```
    try:
        path = _write_tracklist(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
```

New text:

```
    try:
        path = _tracklist_path(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
```

### `r925.S4_write_failure_refuses`

A tracklist that cannot be written raises out of intake set after the job is queued

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r925.json`, row `S4_write_failure_refuses`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`

Old text:

```
    try:
        path = _write_tracklist(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
```

New text:

```
    try:
        path = _write_tracklist(out, held, result)
    except ValueError as exc:
        failed = _tracklist_path(out, held, result)
```

### `r925.S5_unwritten_note_names_no_job_show`

The unwritten note no longer names the verb that lists the tracks

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r925.json`, row `S5_unwritten_note_names_no_job_show`
- Moved: the same unwritten tracklist note of _set_tracklist, which U307 moved from cli.py to cli_identify.py, one level less indented
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`

Old text:

```
f"{exc.strerror or exc}); the job is queued, and its tracks are listed "
            f"by: crate job show {job_id}"
```

New text:

```
f"{exc.strerror or exc}); the job is queued"
```

### `u103-b.C10_open_question_is_pending`

Exit OK from identify while a version question is open

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C10_open_question_is_pending`
- Moved: the same envelope of intake identify, which U307 moved from cli.py to cli_identify.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK,
        pending=pending,
```

New text:

```
        outcome=Outcome.OK,
        code=ExitCode.OK,
        pending=None,
```

### `u103-b.C14_offered_under_its_own_key`

Offer identify's version questions under the match verb's key instead of its own

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C14_offered_under_its_own_key`
- Moved: the text moved whole from intake/cli.py to intake/cli_identify.py with its function (U307); the tests that killed it, test_identify_reports_an_owned_track_owned_an_offered_one_offered_and_the_rest_missing, were folded by the trim into test_identify_and_a_set_job_report_owned_offered_and_missing, every one of its eight checks, carried whole beside the set job's
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
        cfg, result.rows, handler_key=ctx.entry.handler_key, run_id=ctx.run.run_id
```

New text:

```
        cfg, result.rows, handler_key="match.run", run_id=ctx.run.run_id
```

### `u103-b.C3_out_must_be_a_folder`

Drop the check, made before the spend, that --out is not a file

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C3_out_must_be_a_folder`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_tracklist_folder_that_is_a_file_is_refused_before_any_spend`

Old text:

```
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no tracklist can be written into "
```

New text:

```
    if False:
        raise _unusable(
            f"{out} exists and is not a folder, so no tracklist can be written into "
```

### `u103-b.C6_served_note`

Never say that chunks were answered from the cache

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C6_served_note`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`

Old text:

```
    if result.cached:
        notes.append(
```

New text:

```
    if False:
        notes.append(
```

### `u103-b.C7_unwritten_note`

Never say that the answers a pass paid for could not be kept

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C7_unwritten_note`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_answers_that_could_not_be_kept_are_said_on_both_verbs`

Old text:

```
    if result.cache_unwritten:
        notes.append(
```

New text:

```
    if False:
        notes.append(
```

### `u103-b.C9_refusal_counts_the_gap`

Let the unwritable tracklist refusal promise a free rerun over chunks that got no answer

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C9_refusal_counts_the_gap`
- Moved: the text moved whole from intake/cli.py to intake/cli_identify.py with its function (U307); the tests that killed it, test_the_unwritable_tracklist_refusal_does_not_promise_a_free_rerun_over_a_gap, were folded by the trim into test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept, both of its checks, carried whole
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`

Old text:

```
        elif result.unreached:
```

New text:

```
        elif False:
```

### `u104-d.C2_refusal_named_for_the_address`

Let a refusal raised inside the identifier through as it is, naming the scratch file in its message and detail

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C2_refusal_named_for_the_address`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`

Old text:

```
                raise _named_for_the_address(exc, held) from exc.__cause__
```

New text:

```
                raise
```

### `u104-d.C3_detail_renamed`

Rename the message only and leave the scratch path in the refusal's detail

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C3_detail_renamed`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`

Old text:

```
        key: held.ref if value == str(held.path) else value
```

New text:

```
        key: value
```

### `u104-d.C4_scratch_left_said`

Never say that a scratch folder outlived its pass

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C4_scratch_left_said`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`

Old text:

```
    if held.leftover is None:
        return ()
```

New text:

```
    if held.leftover is None or True:
        return ()
```

### `u104-d.C5_no_digest_token_is_the_address`

Take a digestless tracklist's token from the scratch path, which every fetched mix shares, instead of from the address

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C5_no_digest_token_is_the_address`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetched_mix_with_no_digest_is_named_by_its_address_and_not_its_scratch_file`

Old text:

```
    token = digest or digest_of({"path": held.ref})
```

New text:

```
    token = digest or digest_of({"path": str(held.path)})
```

### `u104-e.E2_timeout_is_retryable`

Stop calling a timed out download retryable, the one fetch failure known to be worth running again

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-e.json`, row `E2_timeout_is_retryable`
- Moved: the text moved whole from intake/cli.py to intake/cli_identify.py with its function (U307); the tests that killed it, test_a_download_that_timed_out_is_the_one_fetch_failure_called_retryable, were folded by the trim into test_a_fetch_failure_refuses_and_leaves_no_scratch_file, the timeout case of the parametrized fetch failure test, which asserts retryable only for the timeout
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[timed-out]`

Old text:

```
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            steps=(
                "run it again later",
```

New text:

```
            remedy=Remedy.RETRY_LATER,
            retryable=False,
            steps=(
                "run it again later",
```

### `u104-e.E4_identify_library_before_fetch`

Drop intake identify's check that the library is there to be asked, which runs before anything is fetched or sent

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-e.json`, row `E4_identify_library_before_fetch`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_identify_over_a_url_refuses_an_absent_library_before_anything_is_fetched`
  - `tests/intake/test_workers.py::test_an_absent_library_is_refused_before_the_spend_and_never_read_as_an_empty_one`

Old text:

```
    _library_or_refuse(cfg, shown)

```

New text:

```
(empty)
```

### `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero`

A set where chunks got no answer and the rest named nothing is reported as nothing identified

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u57-recognition-and-items.json`, row `C6_unanswered_zero_reads_as_zero`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`

Old text:

```
    if not result.unreached:
        return ()
    if not result.rows:
        raise refuse(
```

New text:

```
    if not result.unreached or not result.rows:
        return ()
    if False:
        raise refuse(
```

### `u112-b.C7_outcome_always_ok`

A run that wrote nothing ends OK rather than as a no-op

- File: `src/cratekit/organize/cli.py`
- Source: `u112-b.json`, row `C7_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_run_that_writes_nothing_ends_as_a_no_op`

Old text:

```
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u112.C1_report_asks`

--report no longer returns before the gates, so a report asks and may write

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C1_report_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 52 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_registry_the_profile_does_not_use_does_not_refuse_the_filing`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    if report:
        data = _report(areas, report=True, answers={})
```

New text:

```
    if False:
        data = _report(areas, report=True, answers={})
```

### `u112.C5_unexpected_failure_stops`

A step failing in a way the build does not expect stops every later approved step

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C5_unexpected_failure_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after`

Old text:

```
            step.error = refuse(
                "internal-error",
```

New text:

```
            raise
            step.error = refuse(
                "internal-error",
```

### `u112.C6_failure_never_raised`

An approved step that failed is never raised, so the run reads as a clean organize

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C6_failure_never_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[False]`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[True]`
  - `tests/test_organize.py::test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after`

Old text:

```
    if not failed:
        return
    wrote = [
```

New text:

```
    if True:
        return
    wrote = [
```

### `u137.C1_named_always`

Plan an area none of whose kinds is named

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C1_named_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 17 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return selection(kinds, only) != ()
```

New text:

```
    return True
```

### `u137.C2_only_dropped`

Read --only and then plan as if it were absent

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C2_only_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 23 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    only = frozenset(chosen) if chosen else None
```

New text:

```
    only = None
```

### `u137.C3_choices_dropped`

Let the parser take any word as a kind

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C3_choices_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_unknown_kind_is_refused_by_name_before_anything_is_read`

Old text:

```
        choices=KINDS,

```

New text:

```
(empty)
```

### `u222.M21_cli_message_unchanged`

_ask: keep the gate's bare message on a stale answer

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M21_cli_message_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_without_the_frozen_plan_the_same_two_acts_are_refused_stale`

Old text:

```
                message=f"{cause.message}; {area.name}: " + "; ".join(area.stale),
```

New text:

```
                message=cause.message,
```

### `u222.M22_cli_detail_unchanged`

_ask: carry no stale lines in the refusal's detail

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M22_cli_detail_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`

Old text:

```
                detail={**dict(cause.detail or {}), "stale": list(area.stale)},
```

New text:

```
                detail=cause.detail,
```

### `u222.M23_cli_empty_stale_reworded`

_ask: reword a stale refusal whose area has nothing to add

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M23_cli_empty_stale_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied`

Old text:

```
        if exc.cause.code != ExitCode.DECISION_STALE or not area.stale:
```

New text:

```
        if exc.cause.code != ExitCode.DECISION_STALE:
```

### `u267.M1_report_shares_nothing`

organize: the report makes no shared read, so every reader opens its own handle again, seven opens

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M1_report_shares_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 149 against a baseline of 149
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_report_reads_inspiration_twice_through_one_handle_and_locks_nothing_meanwhile`
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    one_read = rb_writer.SharedRead(cfg) if report else None
```

New text:

```
    one_read = None
```

### `u267.M2_applying_run_shares`

organize: the run that answers a gate makes a shared read too, so its plans read through one handle

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M2_applying_run_shares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
    one_read = rb_writer.SharedRead(cfg) if report else None
```

New text:

```
    one_read = rb_writer.SharedRead(cfg)
```

### `u267.M3_report_never_closes`

organize: the finally closes no shared read, so the report leaves its handle and engine open

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M3_report_never_closes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 111 against a baseline of 111
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if one_read is not None:
            one_read.close()
```

New text:

```
        if one_read is not None:
            pass
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

### `r1476.M10_no_name_slug_step`

_label_seam: drop the name slug step, so Some*Label no longer names Some Label

- File: `src/cratekit/tagging/cli.py`
- Source: `r1476.json`, row `M10_no_name_slug_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`

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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`

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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_tag_names_one_label_by_its_name_its_slug_or_the_name_it_was_registered_under`

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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_one_label_holds_exactly_is_never_lost_to_a_slug_it_shares`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
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
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 286 against a baseline of 286
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_is_read_as_a_name_before_an_identifier`
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

### `u240.M14_widest_any`

copyright_matcher: the longer needle wins when it carries any other named, not every other

- File: `src/cratekit/tagging/cli.py`
- Source: `u240.json`, row `M14_widest_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 338 against a baseline of 338
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
- Collected: 338 against a baseline of 338
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

