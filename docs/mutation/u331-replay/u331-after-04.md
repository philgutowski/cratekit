# Mutation table: u331-after-04

Measured by `scripts/mutate.py` on 2026-11-24 02:36 UTC, branch `HEAD` at `717cc2c3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23132 collected. pytest invocations for this batch: 164.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 02:36 UTC for commit `717cc2c333e3`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 35, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23132 against 23132. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u167.M23_waiting_exit` | `src/cratekit/intake/check_cli.py` | user | 1 file(s) | 71 | 7 | killed |
| `u167.M24_suspect_exit` | `src/cratekit/intake/check_cli.py` | user | 1 file(s) | 71 | 5 | killed |
| `u327.B3_partial_apply_refuses` | `src/cratekit/analysis/head_adopt_cli.py` | user | 1 file(s) | 114 | 3 | killed |
| `r227.C5_favorites_limit_spelled` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 239 | 1 | killed |
| `r228-operator.D11_non_pink_outside` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `r228-operator.D12_missing_pink_queued` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `r228-operator.D4_union_playlist_first` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D5_pink_missing_dropped` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `r228-operator.D6_empty_after_colour` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D7_colour_unread_warned` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D8_from_colour_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 5 | killed |
| `r228-operator.D9_from_playlist_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `r424.B1_colored_key` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 239 | 1 | killed |
| `r424.B3_resume_standing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 239 | 3 | killed |
| `r856-a.F10_concluded_passed` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F11_warning_total` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F1_hearted_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F2_already_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F3_unmatched_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F4_listing_dropped` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F5_listing_off_reasons` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F6_no_match_sentence` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 2 | killed |
| `r856-a.F7_names_from_listing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F8_item_listing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `r856-a.F9_item_reason_carried` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 178 | 1 | killed |
| `u51-item-derivation.A1b_colour_writer_passed` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `u51-item-derivation.H2_hearts_item_not_payload` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 123 | 14 | killed |
| `r1255.N1_landings_of_pass_refuses` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 84 | 2 | killed |
| `r1255.N2_landed_passes_refuses` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 84 | 1 | killed |
| `r746-b.N2_base_drive_swap_disabled` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 44 | 2 | killed |
| `r746-b.N5_present_file_planned_as_an_add` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 44 | 3 | killed |
| `r770-d.C7_unresolved_target_planned_as_an_add` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 77 | 1 | killed |
| `r777.N15_any_pass` | `src/cratekit/intake/native_plan.py` | user | 6 file(s) | 197 | 2 | killed |
| `u113-c.C5_removed_node_holds_name` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 16 | 1 | killed |
| `u120.N4_skipped_is_raised` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 13 | 2 | killed |
| `u126.F1_read_always` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 210 | 1 | killed |
| `u126.P1_no_read` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 210 | 7 | killed |
| `u127.N1_cut_strict` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 2 | killed |
| `u127.N2_every_add_tagged` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 5 | killed |
| `u127.N3_default_cut_when_uncalibrated` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 2 | killed |
| `u127.N4_unreadable_refuses` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 1 | killed |
| `u127.N5_no_category_check` | `src/cratekit/intake/native_plan.py` | user | 9 file(s) | 253 | 1 | killed |
| `u128-b.N4_native_dropped_left_lost` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 210 | 1 | killed |
| `u135.A13_live_inbox_ignores_parent` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 9 | 1 | killed |
| `u135.A4_live_inbox_named_always_false` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A5_recorded_inbox_skips_job_key` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 9 | 1 | killed |
| `u135.A7_leftover_joins_numbered_twin` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 1 | 1 | killed |
| `u146-c.N1_owned_held_planned` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-c.N4_owned_needs_a_heart_file` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 12 | 1 | killed |
| `u157.N1_writable_unasked` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 129 | 1 | killed |
| `u163.W10_search_convention` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W11_search_tie` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W1_words_planned` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 10 | killed |
| `u163.W2_first_value` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W3_year_digits` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 2 | killed |
| `u163.W5_album_artist_mint` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 1 | killed |
| `u163.W6_album_by_artist` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 275 | 1 | killed |
| `u166.A1_parent_check` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 185 | 1 | killed |
| `u166.A2_removed_check` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 185 | 2 | killed |
| `u166.A3_plain_check` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 185 | 1 | killed |
| `u166.A9_reserved_batch` | `src/cratekit/intake/native_plan.py` | user | 7 file(s) | 185 | 1 | killed |
| `u174.N1_landed_passes_closed` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 210 | 1 | killed |
| `u174.N2_landed_passes_committed` | `src/cratekit/intake/native_plan.py` | user | 3 file(s) | 210 | 1 | killed |
| `u174.N3_landed_passes_workflow` | `src/cratekit/intake/native_plan.py` | maintainer | 3 file(s) | 210 | 1 | killed |
| `u174.N4_landed_passes_pass_key` | `src/cratekit/intake/native_plan.py` | maintainer | 3 file(s) | 210 | 1 | killed |
| `r154-a.A1_stamp_pattern` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 189 | 1 | killed |
| `r154-a.A2_stamp_calendar` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 189 | 1 | killed |
| `r154-a.A4_legacy_spelling` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 189 | 1 | killed |
| `r154-b.B11_marker_name_safety` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 5 | killed |
| `r154-b.B9_marker_failure_fails_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 1 | killed |
| `r221-a.E1_outcome_forgets_the_run` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 5 | killed |
| `r221-a.E2_outcome_payload_drops_the_key` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 7 | killed |
| `r222-a.A10_plan_text_at_keep_zero` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 189 | 1 | killed |
| `r222-a.A1_nothing_held` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 5 | killed |
| `r222-a.A2_boundary_not_strict` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 3 | killed |
| `r222-a.A3_no_floor_holds_nothing` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 2 | killed |
| `r222-a.A4_keep_zero_holds` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 1 | killed |
| `r222-a.A5_held_run_takes_no_slot` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 5 | killed |
| `r222-a.A6_any_destination_is_a_floor` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 1 | killed |
| `r222-a.A7_no_record_is_a_late_floor` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 2 | killed |
| `r222-a.A8_floor_read_by_a_rehearsal` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 3 | killed |
| `r222-a.A9_rehearsal_purges` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 4 | killed |
| `r338-a.B7_rehearsal_transfers_the_share` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 1 | killed |
| `r338-b.R2_missing_directory_exit_moved` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 1 | killed |
| `r338-c.C3_rehearsed_restore_pulls_the_share` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 1 | killed |
| `r349-c.C1_prune_recorded` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 29 | killed |
| `r349-c.C4_argv_rendered` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 4 | killed |
| `r367.E1_a_failed_transfer_is_unread` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 283 | 15 | killed |
| `r388-c.M17_slug_respelled` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 4 | killed |
| `u311.A1_warning_key_order` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u311.A2_refused_portion_runs` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u311.A3_database_destination_not_required` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u311.A4_logged_takes_any_json` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u45-round-1.E1_rehearsal_publishes` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 7 | killed |
| `u45-round-1.E2_publish_unconditional` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 7 | killed |
| `u45-round-1.E4_return_codes_unread` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 16 | killed |
| `u45-round-2.E5_outcome_ok_widened` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 1 | killed |
| `u48-author.E1_listing_return_code_inverted` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 17 | killed |
| `u48-author.P1_listing_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 4 | killed |
| `u48-author.P2_purge_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 1 | killed |
| `u48-author.P3_two_codes_collapsed_to_one` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 229 | 2 | killed |
| `u48-author.P4_warning_not_recorded_on_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 5 | killed |
| `u48-author.P6_purge_count_not_named` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 1 | killed |
| `u48-author.P7_listing_message_reworded` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 1 | killed |
| `u292.M01_floor` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M02_proposed_needs_a_write` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 3 | killed |
| `u292.M03_served_needs_a_write` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 3 | killed |
| `u292.M04_file_word_routes_first` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 8 | killed |
| `u292.M05_coarse_never_hides_specific` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 7 | killed |
| `u292.M06_source_names_the_genre_voted` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M07_alias_needs_agreement` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 2 | killed |
| `u292.M08_alias_rows_need_an_entry` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 3 | killed |
| `u292.M09_folder_counts_by_the_row` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 2 | killed |
| `u292.M10_unread_counted` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M11_joining_files_nowhere` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M12_folder_threshold` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M13_neighbours_declared_only` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M14_alias_moving_nothing` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 1 | killed |
| `u292.M15_settled_rows_reached` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 1081 | 2 | killed |
| `u294.M26_needing_disposition` | `src/cratekit/tagging/backlog.py` | user | 2 file(s) | 118 | 5 | killed |
| `u322.M23_backlog_row_digest_keeps_words` | `src/cratekit/tagging/backlog.py` | user | 6 file(s) | 392 | 1 | killed |
| `sitting3.G8_queue_skips_readiness` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 2 | killed |
| `u181.C3_unscored_flag_ignored` | `src/cratekit/vocals/cli.py` | user | 2 file(s) | 107 | 5 | killed |
| `u25.G6_always_rewrite` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `u181.C1_unscored_head_or_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 4 | killed |
| `u181.C2_unscored_ignores_score` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 4 | killed |
| `u93-recursive-analysis.D23_vocals_resume_warning` | `src/cratekit/vocals/cli.py` | user | 1 file(s) | 36 | 1 | killed |
| `u93-recursive-analysis.D25_vocals_join` | `src/cratekit/vocals/cli.py` | maintainer | 1 file(s) | 36 | 1 | killed |

## Row definitions

### `u167.M23_waiting_exit`

analyze_check: waiting ends ok with exit 0 rather than pending

- File: `src/cratekit/intake/check_cli.py`
- Source: `u167.json`, row `M23_waiting_exit`
- Moved: the same text, now in src/cratekit/intake/check_cli.py, was in src/cratekit/analysis/check_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
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

- File: `src/cratekit/intake/check_cli.py`
- Source: `u167.json`, row `M24_suspect_exit`
- Moved: the same text, now in src/cratekit/intake/check_cli.py, was in src/cratekit/analysis/check_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
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

### `u327.B3_partial_apply_refuses`

analyze_adopt: end a run whose files did not all take as ok

- File: `src/cratekit/analysis/head_adopt_cli.py`
- Source: `u327.json`, row `B3_partial_apply_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_that_cannot_be_written_keeps_its_row_s_title_and_is_named`
  - `tests/test_analyze_adopt.py::test_a_file_that_does_not_read_back_keeps_its_row_s_title_and_is_named`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`

Old text:

```
    if written is None or not (written.files.failed or written.files.wrong):
```

New text:

```
    if True:
```

### `r227.C5_favorites_limit_spelled`

sync favorites judges against a seven spelled in the shell

- File: `src/cratekit/favorites/cli.py`
- Source: `r227.json`, row `C5_favorites_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `r228-operator.D11_non_pink_outside`

union_with_pink: queue every export row, not only pink and playlist

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D11_non_pink_outside`
- Moved: The two dedup loops of union_with_pink became one dict.fromkeys over the playlist then the pink rows the export carries; the second source swapped for every export row the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        track_ids=tuple(dict.fromkeys([*playlist.track_ids, *in_export])),
```

New text:

```
        track_ids=tuple(dict.fromkeys([*playlist.track_ids, *library.entries])),
```

### `r228-operator.D12_missing_pink_queued`

union_with_pink: queue pink rows the export lacks

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D12_missing_pink_queued`
- Moved: The loop that split pink rows by whether the export carries them became a comprehension; the same membership test, dropped so every pink row is queued.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`

Old text:

```
    in_export = [track_id for track_id in pink_ids if track_id in library.entries]
```

New text:

```
    in_export = [track_id for track_id in pink_ids]
```

### `r228-operator.D4_union_playlist_first`

union_with_pink: emit pink only rows before playlist members

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D4_union_playlist_first`
- Moved: The two dedup loops became one dict.fromkeys whose order is the playlist then the pink rows; the same order, swapped so pink only rows come first.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
        track_ids=tuple(dict.fromkeys([*playlist.track_ids, *in_export])),
```

New text:

```
        track_ids=tuple(dict.fromkeys([*in_export, *playlist.track_ids])),
```

### `r228-operator.D5_pink_missing_dropped`

union_with_pink: drop pink rows the export lacks instead of naming them

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D5_pink_missing_dropped`
- Moved: The else branch that named a pink row the export lacks became the pink_missing comprehension; emptied the same way, so the missing rows are dropped instead of named.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`

Old text:

```
        pink_missing=tuple(track_id for track_id in pink_ids if track_id not in library.entries),
```

New text:

```
        pink_missing=(),
```

### `r228-operator.D6_empty_after_colour`

resolve_sweep: read colour before resolving the playlist, so empty All Favorites is rescued by pink

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D6_empty_after_colour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_resolve_sweep_refuses_empty_favorites_before_colour`

Old text:

```
    library = source.read_library(exported)
    resolved = source.resolve(library, wanted)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)
```

New text:

```
    library = source.read_library(exported)
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    try:
        resolved = source.resolve(library, wanted)
    except Exception:
        resolved = source.ResolvedPlaylist(key=wanted, name=wanted, track_ids=())
    return exported, union_with_pink(library, resolved, pink_ids)
```

### `r228-operator.D7_colour_unread_warned`

resolve_sweep: swallow a colour read refusal and sweep the playlist alone

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D7_colour_unread_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_resolve_sweep_propagates_the_colour_reads_own_cause`

Old text:

```
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        pink_ids = read_pink_track_ids(loaded)
    return exported, union_with_pink(library, resolved, pink_ids)
```

New text:

```
    if pink_ids is None:
        loaded = cfg if cfg is not None else shell.load_config("favorites.cli")
        try:
            pink_ids = read_pink_track_ids(loaded)
        except Exception:
            pink_ids = ()
    return exported, union_with_pink(library, resolved, pink_ids)
```

### `r228-operator.D8_from_colour_zero`

union_with_pink: always report from_colour as zero

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D8_from_colour_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 5 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_names_pink_rows_the_export_lacks`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        from_colour=len(in_export),
```

New text:

```
        from_colour=0,
```

### `r228-operator.D9_from_playlist_zero`

union_with_pink: always report from_playlist as zero

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D9_from_playlist_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`
  - `tests/test_favorites_pink.py::test_the_gate_names_colour_and_playlist_counts`
  - `tests/test_favorites_pink.py::test_union_leaves_non_pink_outside_playlist_out`
  - `tests/test_favorites_pink.py::test_union_offers_pink_outside_playlist_and_keeps_playlist_non_pink`

Old text:

```
        from_playlist=len(playlist.track_ids),
```

New text:

```
        from_playlist=0,
```

### `r424.B1_colored_key`

Restore the always empty colored key on each item report

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B1_colored_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 239 against a baseline of 239
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`

Old text:

```
        "already": list(report.already),
        "unmatched": list(report.unmatched),
```

New text:

```
        "already": list(report.already),
        "colored": list(report.colored),
        "unmatched": list(report.unmatched),
```

### `r424.B3_resume_standing`

Stop passing the standing warning into the resume branch

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B3_resume_standing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 239 against a baseline of 239
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_the_resumed_sweep_says_the_same_thing_where_the_hearting_actually_happens`

Old text:

```
            standing=local_write_warning(),
```

New text:

```
(empty)
```

### `r856-a.F10_concluded_passed`

favorites.sync_favorites: pass no concluded hook to the resume, so a sweep with unmatched favourites carries no warning

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F10_concluded_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            concluded=concluded,
```

New text:

```
            concluded=None,
```

### `r856-a.F11_warning_total`

favorites.concluded: state the unmatched count as the total, so the warning says 1 of the 1

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F11_warning_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_the_sweep_warning_counts_only_whole_numbers`

Old text:

```
                f"{missed} of the {total} favourite(s) in this sweep were not "
```

New text:

```
                f"{missed} of the {missed} favourite(s) in this sweep were not "
```

### `r856-a.F1_hearted_count`

favorites.summary: count hearted as the already list's length, so the answer's hearted count is the wrong list

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F1_hearted_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            "hearted": len(hearted),
```

New text:

```
            "hearted": len(already),
```

### `r856-a.F2_already_count`

favorites.summary: count already hearted as zero, so a favourite hearted before is counted nowhere

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F2_already_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`

Old text:

```
            "already_hearted": len(already),
```

New text:

```
            "already_hearted": 0,
```

### `r856-a.F3_unmatched_count`

favorites.summary: count unmatched as the reason sentences, so a favourite the account said nothing about is not counted

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F3_unmatched_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            "unmatched": len(unmatched),
```

New text:

```
            "unmatched": len(reasons),
```

### `r856-a.F4_listing_dropped`

favorites.summary: build each item's unmatched rows but never list them, so the answer counts a favourite it does not name

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F4_listing_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
        left_out.extend(_left_out(report, said))
```

New text:

```
        pass
```

### `r856-a.F5_listing_off_reasons`

favorites._left_out: list the rows reasons names instead of every unmatched row, so a favourite with no reason is left out

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F5_listing_off_reasons`
- Moved: The loop over the report's unmatched list now takes each identity as text directly; the same source, swapped for the rows the reasons name the same way.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_report_written_before_the_listing_still_names_its_unmatched_rows`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    for identity in map(str, report.get("unmatched") or ()):
```

New text:

```
    for identity in map(str, [one.get("row") for one in said]):
```

### `r856-a.F6_no_match_sentence`

favorites._left_out: leave the reason empty when the account gave none, so the line reads no reason given

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F6_no_match_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_report_written_before_the_listing_still_names_its_unmatched_rows`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
                "reason": str(one.get("reason") or "") or NO_MATCH,
```

New text:

```
                "reason": str(one.get("reason") or ""),
```

### `r856-a.F7_names_from_listing`

favorites._left_out: read names off reasons alone, so a new report's unmatched row with no reason has no artist or title

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F7_names_from_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    for one in (*said, *(report.get("unmatched_tracks") or ())):
```

New text:

```
    for one in said:
```

### `r856-a.F8_item_listing`

favorites.run_heart_item: commit no unmatched_tracks, so an artifact names no unmatched row the account said nothing about

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F8_item_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
        "unmatched_tracks": [row_named(row, said.get(row, "")) for row in report.unmatched],
```

New text:

```
        "unmatched_tracks": [],
```

### `r856-a.F9_item_reason_carried`

favorites.run_heart_item: list every unmatched row with an empty reason, so the account's reason is lost from the listing

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F9_item_reason_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`

Old text:

```
        "unmatched_tracks": [row_named(row, said.get(row, "")) for row in report.unmatched],
```

New text:

```
        "unmatched_tracks": [row_named(row, "") for row in report.unmatched],
```

### `u51-item-derivation.A1b_colour_writer_passed`

Pass a REAL colour writer, which A1 could not: colors=None is the engine's own default, so removing the keyword changed nothing

- File: `src/cratekit/favorites/cli.py`
- Source: `u51-item-derivation.json`, row `A1b_colour_writer_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`

Old text:

```
    report = hearts.heart_back(cfg, remote, candidates, colors=None)
```

New text:

```
    class _Pink:
        def color_pink(self, row_id):
            return None

        def is_pink(self, row_id):
            return False

    report = hearts.heart_back(cfg, remote, candidates, colors=_Pink())
```

### `u51-item-derivation.H2_hearts_item_not_payload`

The sweep handler reads the playlist key as its row, not the claimed item

- File: `src/cratekit/favorites/cli.py`
- Source: `u51-item-derivation.json`, row `H2_hearts_item_not_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_the_handler_runs_against_the_frozen_configuration_not_the_current_one[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_resumed_sweep_says_the_same_thing_where_the_hearting_actually_happens`
  - `tests/test_outbound_workers.py::test_the_sweep_reaches_nothing_outside_the_add_only_protocol`

Old text:

```
    report = run_heart_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_heart_item(payload, str(payload[PLAYLIST]), cfg, account.resolve(cfg))
```

### `r1255.N1_landings_of_pass_refuses`

native.landings_of_pass: drop the unread half again, so sync mark says a recorded landing never committed

- File: `src/cratekit/intake/native_plan.py`
- Source: `r1255.json`, row `N1_landings_of_pass_refuses`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_sync_mark.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_landing`

Old text:

```
    land the pass again.
    """
    records = session.records(cfg)
```

New text:

```
    land the pass again.
    """
    records = session.scan_log(cfg)[0]
```

### `r1255.N2_landed_passes_refuses`

native.landed_passes: drop the unread half again, so organize plans no native pass over a log it could not list

- File: `src/cratekit/intake/native_plan.py`
- Source: `r1255.json`, row `N2_landed_passes_refuses`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`

Old text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.records(cfg)
```

New text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.scan_log(cfg)[0]
```

### `r746-b.N2_base_drive_swap_disabled`

stored_folder_path: the mounted path is stored whatever the property table records

- File: `src/cratekit/intake/native_plan.py`
- Source: `r746-b.json`, row `N2_base_drive_swap_disabled`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_stored_path_is_nfc_and_the_swap_is_anchored_on_a_whole_component`

Old text:

```
        if text == current or text.startswith(current + os.sep):
```

New text:

```
        if False:
```

### `r746-b.N5_present_file_planned_as_an_add`

plan_rows: a file the collection already holds is planned as an add, so it would be added twice

- File: `src/cratekit/intake/native_plan.py`
- Source: `r746-b.json`, row `N5_present_file_planned_as_an_add`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`

Old text:

```
            action, why = (ADD if held is None else PRESENT), ""
```

New text:

```
            action, why = ADD, ""
```

### `r770-d.C7_unresolved_target_planned_as_an_add`

native.plan_rows: read a target the matcher could not resolve as a file the collection does not hold

- File: `src/cratekit/intake/native_plan.py`
- Source: `r770-d.json`, row `C7_unresolved_target_planned_as_an_add`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_engine_refuses_a_target_it_cannot_resolve_instead_of_planning_an_add`

Old text:

```
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
```

New text:

```
        if False:
```

### `r777.N15_any_pass`

landings_of_pass counts a landing of another pass

- File: `src/cratekit/intake/native_plan.py`
- Source: `r777.json`, row `N15_any_pass`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`

Old text:

```
            and record.detail.get(PASS_KEY) == name

```

New text:

```
(empty)
```

### `u113-c.C5_removed_node_holds_name`

A removed node under INBOX still holds its name, so a free exact name takes a count

- File: `src/cratekit/intake/native_plan.py`
- Source: `u113-c.json`, row `C5_removed_node_holds_name`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
        if not rb_writer.node_removed(row):
```

New text:

```
        if True:
```

### `u120.N4_skipped_is_raised`

_favorites_plan: a home that cannot be resolved raises through the landing

- File: `src/cratekit/intake/native_plan.py`
- Source: `u120.json`, row `N4_skipped_is_raised`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    try:
        home = placement.resolve_home(db, source)
    except CratekitError as exc:
```

New text:

```
    try:
        home = placement.resolve_home(db, source)
    except ValueError as exc:
```

### `u126.F1_read_always`

Read the library's link whatever the plan adds, so a landing of held files refuses on a split library

- File: `src/cratekit/intake/native_plan.py`
- Source: `u126.json`, row `F1_read_always`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.library_link(db)
```

### `u126.P1_no_read`

Skip the library read and plan a fixed value, the binding's shape of a guess

- File: `src/cratekit/intake/native_plan.py`
- Source: `u126.json`, row `P1_no_read`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_an_approval_at_one_link_is_not_applied_at_another_and_no_majority_refuses`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.LibraryLink(value=7, carriers=0, rows=0)
        if any(row.action == ADD for row in rows)
        else None
```

### `u127.N1_cut_strict`

Compare the score strictly above the cut, so a file exactly at the cut is not tagged

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N1_cut_strict`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut + 0.5)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

### `u127.N2_every_add_tagged`

Tag every added row whatever its score, the guess the brief forbids

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N2_every_add_tagged`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[below]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[zero]`
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        scored.append(replace(row, voxlevel=level, vox=True))
```

### `u127.N3_default_cut_when_uncalibrated`

Tag from the vocals verb's default cut on a library with no calibration instead of blocking

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N3_default_cut_when_uncalibrated`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
    if cut is None:
        return rows, None, VOX_UNCALIBRATED
```

New text:

```
    if cut is None:
        cut = metadata_cli.DEFAULT_VOCAL_THRESHOLD
```

### `u127.N4_unreadable_refuses`

Let an unreadable calibration refuse the landing rather than block the tag

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N4_unreadable_refuses`
- Moved: the vox guard moved whole from native.py to native_plan.py with the plan (U307); the test that killed it, test_an_unreadable_calibration_tags_nothing_and_lands_the_batch, is now the _unreadable case of test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch in the same file, parametrized over the three blocked shapes with the same input and the same checks
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_unreadable]`

Old text:

```
    except CratekitError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
```

New text:

```
    except ValueError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
```

### `u127.N5_no_category_check`

Skip the writer's question at plan time, so a library with no category fails after the moves

- File: `src/cratekit/intake/native_plan.py`
- Source: `u127.json`, row `N5_no_category_check`
- Moved: the vox guard moved whole from native.py to native_plan.py with the plan (U307); the test that killed it, test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch, is now the _no_category case of test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch in the same file, the same input and the same checks
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`

Old text:

```
    if not rb_writer.my_tag_writable(db):
        return rows, cut, VOX_NO_CATEGORY
```

New text:

```
    if False:
        return rows, cut, VOX_NO_CATEGORY
```

### `u128-b.N4_native_dropped_left_lost`

A native playlist holding nothing writable drops its left rows

- File: `src/cratekit/intake/native_plan.py`
- Source: `u128-b.json`, row `N4_native_dropped_left_lost`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_whose_only_file_is_unsupported_still_names_it_as_left`

Old text:

```
            dropped.extend((one.name, row) for row in left)
```

New text:

```
            pass
```

### `u135.A13_live_inbox_ignores_parent`

live_inbox_named matches the name anywhere, not only under the intake root

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A13_live_inbox_ignores_parent`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True

```

New text:

```
        if True:
            return True

```

### `u135.A4_live_inbox_named_always_false`

Never detect a live set-named INBOX playlist, so a hand-made one reads as made

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A4_live_inbox_named_always_false`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`

Old text:

```
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True
    return False

```

New text:

```
    return False

```

### `u135.A5_recorded_inbox_skips_job_key`

recorded_inbox_playlist ignores the job key so any closed batch playlist is treated as this job's

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A5_recorded_inbox_skips_job_key`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        and record.detail[BATCH_PLAYLIST_KEY].get(INBOX_JOB_KEY) == job_id

```

New text:

```
        and True

```

### `u135.A7_leftover_joins_numbered_twin`

A numbered twin of the set name under INBOX is no longer named as a leftover

- File: `src/cratekit/intake/native_plan.py`
- Source: `u135.json`, row `A7_leftover_joins_numbered_twin`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`

Old text:

```
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)

```

New text:

```
        if False:
            named.append(held)

```

### `u146-c.N1_owned_held_planned`

_favorites_plan: an owned heart All Favorites holds is planned again beside a landing, and its month made

- File: `src/cratekit/intake/native_plan.py`
- Source: `u146-c.json`, row `N1_owned_held_planned`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_is_no_write_beside_a_landing`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`

Old text:

```
        if one.content_id in in_source or one.content_id in seen:
```

New text:

```
        if one.content_id in seen:
```

### `u146-c.N4_owned_needs_a_heart_file`

_favorites_plan: owned hearts are placed only when a landed file is a heart too

- File: `src/cratekit/intake/native_plan.py`
- Source: `u146-c.json`, row `N4_owned_needs_a_heart_file`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`

Old text:

```
    if not (kept or owned) or not source:
```

New text:

```
    if not kept or not source:
```

### `u157.N1_writable_unasked`

_dyn_plan: skip the writer's own question, so a library with no category to copy plans a tag the commit refuses

- File: `src/cratekit/intake/native_plan.py`
- Source: `u157.json`, row `N1_writable_unasked`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    if not rb_writer.my_tag_writable(db):
        return read, cut, DYN_NO_CATEGORY

```

New text:

```
(empty)
```

### `u163.W10_search_convention`

_Resolver._shaped: store NULL in SearchStr whatever the library's convention

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W10_search_convention`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_mint_follows_the_librarys_searchstr_convention`

Old text:

```
        return replace(word, search=word.name if convention == SEARCH_NAME else convention)
```

New text:

```
        return replace(word, search=None)
```

### `u163.W11_search_tie`

search_convention: answer the first ranked convention on a tie

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W11_search_tie`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_tied_searchstr_convention_mints_null`

Old text:

```
    if not ranked or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
```

New text:

```
    if not ranked:
```

### `u163.W1_words_planned`

plan_rows: never plan the words, so no row carries artist, album, genre or year

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W1_words_planned`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_words.py::test_a_mint_follows_the_librarys_searchstr_convention`
  - `tests/test_intake_land_words.py::test_a_multi_value_id3_frame_lands_its_first_value_as_the_word`
  - `tests/test_intake_land_words.py::test_a_tied_searchstr_convention_mints_null`
  - `tests/test_intake_land_words.py::test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it_or_else_minted`
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`
  - `tests/test_intake_land_words.py::test_a_word_the_library_holds_links_its_active_row_and_mints_nothing`
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`

Old text:

```
    rows = _words_plan(db, rows)

```

New text:

```
    rows = rows

```

### `u163.W2_first_value`

_word: keep the NUL joined ID3 value whole (round one's fix)

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W2_first_value`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_multi_value_id3_frame_lands_its_first_value_as_the_word`

Old text:

```
    first = (value or "").split("\x00")[0]
```

New text:

```
    first = value or ""
```

### `u163.W3_year_digits`

year_of: accept any four characters as a year

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W3_year_digits`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_year_is_the_four_digits_the_date_tag_opens_with[0000-None]`
  - `tests/test_intake_land_words.py::test_the_year_is_the_four_digits_the_date_tag_opens_with[circa 2021-None]`

Old text:

```
    if len(head) != 4 or not head.isdigit() or int(head) == 0:
```

New text:

```
    if len(head) != 4:
```

### `u163.W5_album_artist_mint`

_active_album_id: look up an album whose album artist is minted, instead of minting it

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W5_album_artist_mint`
- Moved: the album lookup moved whole from native.py to native_plan.py with the plan (U307); the test that killed it, test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none, is now the Three.flac case of test_an_album_links_the_one_its_album_artist_holds in the same file, which asserts the minted album artist holds a new album beside the namesake with none
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`

Old text:

```
    if album_artist is not None and not album_artist.row_id:
        return ""
```

New text:

```
    if False:
        return ""
```

### `u163.W6_album_by_artist`

_active_album_id: find the album by name alone, ignoring its album artist

- File: `src/cratekit/intake/native_plan.py`
- Source: `u163.json`, row `W6_album_by_artist`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`

Old text:

```
        if str(getattr(row, ALBUM_ARTIST, None) or "") == want
```

New text:

```
        if True
```

### `u166.A1_parent_check`

analyze_playlist: take a live Analyze anywhere, not only directly under the root

- File: `src/cratekit/intake/native_plan.py`
- Source: `u166.json`, row `A1_parent_check`
- Moved: the ANALYZE lookup moved whole from native.py to native_plan.py with the plan (U307); the test that killed it, test_an_analyze_playlist_outside_the_root_is_never_written_into, is now the p-elsewhere node of test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into in the same file, the same node and the same check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") != str(root_id):
            continue
        if rb_writer.node_removed(row)
```

New text:

```
        if False:
            continue
        if rb_writer.node_removed(row)
```

### `u166.A2_removed_check`

analyze_playlist: take a removed Analyze as the queue

- File: `src/cratekit/intake/native_plan.py`
- Source: `u166.json`, row `A2_removed_check`
- Moved: the ANALYZE lookup moved whole from native.py to native_plan.py with the plan (U307); the tests that killed it are now the p-gone node of test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into and the removed after approval half of test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses, in the same file, the same inputs and checks
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into`

Old text:

```
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
```

New text:

```
        if int(getattr(row, "Attribute", -1)) != 0:
```

### `u166.A3_plain_check`

analyze_playlist: take a folder or smart playlist named Analyze as the queue

- File: `src/cratekit/intake/native_plan.py`
- Source: `u166.json`, row `A3_plain_check`
- Moved: the ANALYZE lookup moved whole from native.py to native_plan.py with the plan (U307); the test that killed it, test_a_removed_or_smart_node_named_analyze_is_never_written_into, is now test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into in the same file, its p-smart node the same input and check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into`

Old text:

```
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
```

New text:

```
        if rb_writer.node_removed(row):
```

### `u166.A9_reserved_batch`

plan_rows: let a batch take the name Analyze

- File: `src/cratekit/intake/native_plan.py`
- Source: `u166.json`, row `A9_reserved_batch`
- Moved: the reserved batch name check moved whole from native.py to native_plan.py with the plan (U307); the test that killed it, test_a_batch_named_analyze_is_refused_before_the_gate_and_nothing_moves, is now the second half of test_no_analyze_playlist_still_asks_and_a_batch_named_analyze_is_refused in the same file, the same staging, verb and checks
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_no_analyze_playlist_still_asks_and_a_batch_named_analyze_is_refused`

Old text:

```
    if batch == ANALYZE:
```

New text:

```
    if False:
```

### `u174.N1_landed_passes_closed`

landed_passes: drop the closed state check, so an open landing's pass is planned

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N1_landed_passes_closed`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N2_landed_passes_committed`

landed_passes: drop the committed source check, so a refused landing's pass is planned

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N2_landed_passes_committed`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and record.state is session.SessionState.CLOSED
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N3_landed_passes_workflow`

landed_passes: drop the workflow check, so any closed session naming a pass is read as a landing

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N3_landed_passes_workflow`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                if record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N4_landed_passes_pass_key`

landed_passes: drop the pass key check, so a landing of no pass is listed as a pass named None

- File: `src/cratekit/intake/native_plan.py`
- Source: `u174.json`, row `N4_landed_passes_pass_key`
- Moved: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 210 against a baseline of 210
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
            }
```

### `r154-a.A1_stamp_pattern`

Drop the pattern half of is_stamp, so the calendar parse alone decides and its lenient padding admits 2026-8-01T000000Z

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A1_stamp_pattern`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-8-01T000000Z]`

Old text:

```
    if not _STAMP_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _STAMP_FORMAT)
```

New text:

```
    try:
        datetime.strptime(value, _STAMP_FORMAT)
```

### `r154-a.A2_stamp_calendar`

Drop the calendar half of is_stamp, so the pattern alone decides and a thirteenth month is a stamp

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A2_stamp_calendar`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-13-01T000000Z]`

Old text:

```
    try:
        datetime.strptime(value, _STAMP_FORMAT)
    except ValueError:
        return False
    return True
```

New text:

```
    return True
```

### `r154-a.A4_legacy_spelling`

Accept only this product's stamp as a snapshot name, so every snapshot the source system wrote is refused by name and hidden from the listing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A4_legacy_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_the_source_system_wrote_is_still_a_name_and_still_pulled`

Old text:

```
    if is_stamp(value):
        return True
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
```

New text:

```
    if is_stamp(value):
        return True
    return False
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
```

### `r154-b.B11_marker_name_safety`

Write a marker for any identity at all, so one carrying a separator or a dot segment is interpolated into a remote path

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B11_marker_name_safety`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[..]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[.hidden]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has space]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has/slash]`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`

Old text:

```
    if not _MARKER_IDENTITY.fullmatch(folded):
        return None
```

New text:

```
    if False:
        return None
```

### `r154-b.B9_marker_failure_fails_the_portion`

Let a marker that cannot be written fail the database portion, which skips the settings and publishes no age over a good copy

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B9_marker_failure_fails_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup`

Old text:

```
            if result.returncode != 0 and command.label == SNAPSHOT_IDENTITY:
```

New text:

```
            if False and command.label == SNAPSHOT_IDENTITY:
```

### `r221-a.E1_outcome_forgets_the_run`

The outcome records False whatever the run was, which is the state before this unit: a rehearsal and a real run render identically

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E1_outcome_forgets_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_outcome_itself_records_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=dry_run)
```

New text:

```
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=False)
```

### `r221-a.E2_outcome_payload_drops_the_key`

The renderer stops carrying the flag, so every reader of a rendered run is back to guessing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E2_outcome_payload_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_the_outcome_itself_records_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        "dry_run": outcome.dry_run,
        "portions": [
```

New text:

```
        "portions": [
```

### `r222-a.A10_plan_text_at_keep_zero`

Describe the held run at a keep of zero, so the preview promises a retention the run does not apply

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A10_plan_text_at_keep_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_plan_describes_the_rotation_the_run_applies[0-keeping no-last completed mirror]`

Old text:

```
    if archive_keep == 0:
        return "keeping no dated archive folder"
```

New text:

```
    if False:
        return "keeping no dated archive folder"
```

### `r222-a.A1_nothing_held`

Hold nothing, which is the finding itself: the rotation counts attempts again and a retry that succeeds purges the failed attempt's archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A1_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = []
```

### `r222-a.A2_boundary_not_strict`

Hold a folder named exactly at the floor, so the last completed run's own folder is never settled and survives every later run

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A2_boundary_not_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`

Old text:

```
(floor is None or name > floor)]
```

New text:

```
(floor is None or name >= floor)]
```

### `r222-a.A3_no_floor_holds_nothing`

Read no floor as nothing to hold, so a remote with no completed mirror on record is rotated as though every folder were settled

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A3_no_floor_holds_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`

Old text:

```
(floor is None or name > floor)]
```

New text:

```
(floor is not None and name > floor)]
```

### `r222-a.A4_keep_zero_holds`

Hold the run's folders at a keep of zero, overruling a request to keep no archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A4_keep_zero_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = [name for name in names if (floor is None or name > floor)]
```

### `r222-a.A5_held_run_takes_no_slot`

Spend the whole keep on settled folders, so the held run is kept on top of the keep rather than as one slot of it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A5_held_run_takes_no_slot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    slots = keep - 1 if held else keep
```

New text:

```
    slots = keep
```

### `r222-a.A6_any_destination_is_a_floor`

Take the floor from a completed mirror to ANOTHER destination, which says nothing about which folders here are finished

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A6_any_destination_is_a_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`

Old text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
```

New text:

```
    if fact is None:
        return None
```

### `r222-a.A7_no_record_is_a_late_floor`

Answer a missing record with a floor after every date, so nothing is held and the old rotation runs on a remote with no completed mirror

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A7_no_record_is_a_late_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`

Old text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
```

New text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return "9999"
```

### `r222-a.A8_floor_read_by_a_rehearsal`

Read the record above the rehearsal's return, so a preview fails over a file it never touches

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A8_floor_read_by_a_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if keep < 0 or not purge:
        return out, None
    floor = _rotation_floor(cfg)
```

New text:

```
    floor = _rotation_floor(cfg)
    if keep < 0 or not purge:
        return out, None
```

### `r222-a.A9_rehearsal_purges`

EXISTING GUARD, sampled because this round re-armed its tests: a rehearsal runs the real purge

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A9_rehearsal_purges`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
                    purge=not dry_run,
```

New text:

```
                    purge=True,
```

### `r338-a.B7_rehearsal_transfers_the_share`

TRANSFERRING_LABELS: leave the share's capture out, so a dry run really syncs gigabytes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-a.json`, row `B7_rehearsal_transfers_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_rehearsed_backup_transfers_no_share`

Old text:

```
        SNAPSHOT_SHARE,
        RESTORE_MIRROR,
```

New text:

```
        RESTORE_MIRROR,
```

### `r338-b.R2_missing_directory_exit_moved`

RCLONE_DIRECTORY_NOT_FOUND: move the exit to 4, rclone's file not found, a nearby value, so a missing mirror refuses

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-b.json`, row `R2_missing_directory_exit_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_the_share_is_listed_before_anything_is_cleared`

Old text:

```
RCLONE_DIRECTORY_NOT_FOUND = 3
```

New text:

```
RCLONE_DIRECTORY_NOT_FOUND = 4
```

### `r338-c.C3_rehearsed_restore_pulls_the_share`

TRANSFERRING_LABELS: leave the share's restore out, so a rehearsed restore really downloads it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-c.json`, row `C3_rehearsed_restore_pulls_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_rehearsed_restore_transfers_no_share`

Old text:

```
        RESTORE_DATABASE,
        RESTORE_SHARE,
    }
```

New text:

```
        RESTORE_DATABASE,
    }
```

### `r349-c.C1_prune_recorded`

The prune calls the bare runner, so its commands are not recorded beside its results

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C1_prune_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 278 against a baseline of 278
- Kills: 29 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_backup_payload_carries_a_version`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - ... and 14 more, see the JSON sidecar

Old text:

```
                    runner=recorded,
```

New text:

```
                    runner=runner,
```

### `r349-c.C4_argv_rendered`

outcome_payload renders the label where the argv belongs

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C4_argv_rendered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 278 against a baseline of 278
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`

Old text:

```
                        "argv": list(command.argv),
```

New text:

```
                        "argv": [command.label],
```

### `r367.E1_a_failed_transfer_is_unread`

existing guard sample: run_restore returns results without reading return codes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E1_a_failed_transfer_is_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 15 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent`
  - `tests/modules/test_tools.py::test_a_rehearsed_restore_does_not_clear_the_live_sidecars`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_removes_stale_sidecars_before_copying`
  - `tests/modules/test_tools.py::test_the_sidecars_are_cleared_before_the_mirror_too`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

New text:

```
        if result.returncode == 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
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

### `u311.A1_warning_key_order`

The shared warning builder writes message before code, changing every warning's key order in the envelope

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A1_warning_key_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
    return {"code": code, "message": message}
```

New text:

```
    return {"message": message, "code": code}
```

### `u311.A2_refused_portion_runs`

A portion with a refusal still reads as one that will run

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A2_refused_portion_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
        return self.refusal is None and (bool(self.commands) or self.kind in _NOTHING_TO_SEND)
```

New text:

```
        return bool(self.commands) or self.kind in _NOTHING_TO_SEND
```

### `u311.A3_database_destination_not_required`

The destination check forgets the database snapshot root, so a run without it is not refused up front

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A3_database_destination_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
    keys = ("dest", "archive_root", "db_dest_root")
```

New text:

```
    keys = ("dest", "archive_root")
```

### `u311.A4_logged_takes_any_json`

The comparison log reader keeps any JSON value, not only objects

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A4_logged_takes_any_json`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
    return [entry for entry in map(_parsed, stderr.splitlines()) if isinstance(entry, dict)]
```

New text:

```
    return [entry for entry in map(_parsed, stderr.splitlines()) if entry is not None]
```

### `u45-round-1.E1_rehearsal_publishes`

Let a dry run publish, so a preview records a backup age for a run that copied not one byte

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E1_rehearsal_publishes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if dry_run:
        publish = False
```

New text:

```
    pass
```

### `u45-round-1.E2_publish_unconditional`

Publish regardless of the flag, the same hole reached from the other side

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E2_publish_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        if publish:
            backup_facts.record(
```

New text:

```
        if True:
            backup_facts.record(
```

### `u45-round-1.E4_return_codes_unread`

Stop reading return codes in run_backup, which is exactly the defect its sibling run_restore shipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E4_return_codes_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 16 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_capture_marks_the_snapshot_after_the_database_and_never_before_it`
  - `tests/modules/test_tools.py::test_the_prune_runs_only_after_the_mirror_succeeded`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_narrowed_portion_whose_transfer_failed_refuses_by_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`
  - ... and 1 more, see the JSON sidecar

Old text:

```
            if result.returncode != 0:
                failed = result
                break
```

New text:

```
            pass
```

### `u45-round-2.E5_outcome_ok_widened`

Answer ok when ANY portion is fine rather than all of them

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-2.json`, row `E5_outcome_ok_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`

Old text:

```
        return all(p.refusal is not None or p.ran for p in self.portions)
```

New text:

```
        return any(p.refusal is not None or p.ran for p in self.portions)
```

### `u48-author.E1_listing_return_code_inverted`

Existing guard: purge on a failed listing and report a good one as failed

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `E1_listing_return_code_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 17 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_folder_the_last_completed_run_wrote_is_settled_not_held`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing`
  - `tests/modules/test_tools.py::test_the_retention_the_plan_declared_is_the_retention_the_run_applies`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
```

New text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode == 0:
```

### `u48-author.P1_listing_classification_dropped`

A failed listing returns no warning, so the rotation stops silently again

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P1_listing_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

New text:

```
    if result.returncode != 0:
        return out, None
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

### `u48-author.P2_purge_classification_dropped`

Failed purges return no warning, so folders survive with nothing saying so

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P2_purge_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

New text:

```
    if False:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

### `u48-author.P3_two_codes_collapsed_to_one`

One code over both conditions, which is the discriminator this unit split

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P3_two_codes_collapsed_to_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
ARCHIVE_PURGE_FAILED = "archive-purge-failed"
```

New text:

```
ARCHIVE_PURGE_FAILED = "archive-listing-failed"
```

### `u48-author.P4_warning_not_recorded_on_the_portion`

run_backup reads the classification and drops it instead of carrying it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P4_warning_not_recorded_on_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
```

New text:

```
                results += pruned
                continue
```

### `u48-author.P6_purge_count_not_named`

The purge message drops how many folders survived it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P6_purge_count_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
```

New text:

```
                f"the archive rotation did not finish: some dated folder(s) "
```

### `u48-author.P7_listing_message_reworded`

Reword the listing message, not append: the suite asserts with `in`

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P7_listing_message_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`

Old text:

```
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
```

New text:

```
                f"nothing was removed and the rotation will stay stopped "
                f"until it succeeds. The backup itself completed"
```

### `u292.M01_floor`

FLOOR: propose at medium rather than high

- File: `src/cratekit/tagging/backlog.py`
- Source: `u292.json`, row `M01_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_backlog.py`, `tests/test_cli_contract.py`
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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
- Collected: 1081 against a baseline of 1081
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

### `u181.C1_unscored_head_or_score`

analyze vocals --unscored: queue a file carrying the head OR no score, so an unheaded file is queued

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C1_unscored_head_or_score`
- Moved: U343 (b1e44ba9, main) renamed analysis.cli.carries_head to already_measured, the run's resume marker its mark or a head on the name; _unscored still picks a measured file with no score, the same two clause test
- Surface: user
- Subset: test files importing cratekit.vocals.cli
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 4 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
        if analysis_cli.already_measured(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.already_measured(path, cfg) or tags.read_vox_from_file(path) is None:
```

### `u181.C2_unscored_ignores_score`

analyze vocals --unscored: queue every headed file, scored or not

- File: `src/cratekit/vocals/cli.py`
- Source: `u181.json`, row `C2_unscored_ignores_score`
- Moved: U343 (b1e44ba9, main) renamed analysis.cli.carries_head to already_measured, the run's resume marker its mark or a head on the name; _unscored still picks a measured file with no score, the same two clause test
- Surface: user
- Subset: test files importing cratekit.vocals.cli
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 4 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_over_a_folder_whose_headed_files_all_carry_a_score_queues_nothing`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`

Old text:

```
        if analysis_cli.already_measured(path, cfg) and tags.read_vox_from_file(path) is None:
```

New text:

```
        if analysis_cli.already_measured(path, cfg):
```

### `u93-recursive-analysis.D23_vocals_resume_warning`

The vocals resume drops the walk's omissions, the same hole on the other verb

- File: `src/cratekit/vocals/cli.py`
- Source: `u93-recursive-analysis.json`, row `D23_vocals_resume_warning`
- Moved: U331 routes the item list through core.jobs, its listed home, where discovery's names are re-exported; the same call in the same function
- Surface: user
- Subset: test files importing cratekit.vocals.cli
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_vocals_resume_repeats_what_the_walk_left_out`

Old text:

```
        warnings = (*warnings, *jobs.warnings_of(job.payload))
        unscored = _unscored_warning(summary)
```

New text:

```
        unscored = _unscored_warning(summary)
```

### `u93-recursive-analysis.D25_vocals_join`

The vocals worker joins with the operator, the same reversion one file over

- File: `src/cratekit/vocals/cli.py`
- Source: `u93-recursive-analysis.json`, row `D25_vocals_join`
- Moved: U331 routes the item list through core.jobs, its listed home, where discovery's names are re-exported; the same call in the same function
- Surface: maintainer
- Subset: test files importing cratekit.vocals.cli
- Ran: `tests/test_vocals_cli.py`
- Collected: 36 against a baseline of 36
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_vocals_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, jobs.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

