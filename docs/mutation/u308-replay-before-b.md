# Mutation table: u308-replay-before-b

Measured by `scripts/mutate.py` on 2026-11-22 18:27 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 198.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 45, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/5bcab4be-2978-53ef-b3bd-2807d1f5544d/scratchpad/known-failures-plus.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 19 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1634.M10_basis_always_line` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 213 | 1 | killed |
| `r1634.M13_rereader_unguarded` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 213 | 1 | killed |
| `r1634.M14_rereader_beside_a_bare_verifier` | `src/cratekit/label/sweep.py` | maintainer | 2 file(s) | 119 | 1 | killed |
| `r1634.M15_how_reworded` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 213 | 5 | killed |
| `r1634.M18_basis_not_in_detail` | `src/cratekit/label/sweep.py` | user | 2 file(s) | 119 | 1 | killed |
| `r1634.M19_another_act_replaces_a_gone_one` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 1 | killed |
| `r1634.M1_mismatch_mode_always` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 14 | killed |
| `r1634.M20_in_place_note_dropped` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 213 | 1 | killed |
| `r1634.M2_mismatch_mode_never` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 12 | killed |
| `r1634.M3_forced_read_dropped` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 12 | killed |
| `r1634.M4_no_read_confirms` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 2 | killed |
| `r1634.M5_no_read_asks_the_line` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 2 | killed |
| `r1634.M6_gone_not_passed_over` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 3 | killed |
| `r1634.M7_any_answer_passed_over` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 6 | killed |
| `r1634.M8_order_label_line_first` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 4 | killed |
| `r1634.M9_order_other_act_before_label` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 390 | 5 | killed |
| `r259-b.O2_unreadable_row` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r259.L2_library_kwarg` | `src/cratekit/label/sweep.py` | maintainer | 5 file(s) | 524 | 1 | killed |
| `r259.O1_no_tracks_guard` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 22933 | 0 (promoted) | zero |
| `r259.O5_memo` | `src/cratekit/label/sweep.py` | maintainer | 5 file(s) | 22933 | 0 (promoted) | zero |
| `r261.S1_roster_unread_read` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 2 | killed |
| `r261.S2_own_missing` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.S3_source_collects` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 3 | killed |
| `r261.S4_existing_can_list` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 1 | killed |
| `r704-a.S1_no_cause_chain_check` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 6 | killed |
| `r704-a.S2_cause_walk_reads_only_the_error` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S3_no_context_status_check` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S4_context_walk_one_level` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S5_context_read_by_type` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S6_status_coefficient` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S7_probe_unclassified` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S8_crawl_unclassified` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 2 | killed |
| `r704-a.S9_resolve_unclassified` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r790-a.S2_held_is_not_refiled` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 332 | 3 | killed |
| `r790-a.S4_default_is_the_offer` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 332 | 10 | killed |
| `r790-b.S7_first_run_kept` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 332 | 1 | killed |
| `r798-b.G3_a_held_release_takes_a_place` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 316 | 2 | killed |
| `r798-b.G4_a_returned_hold_is_never_judged` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 316 | 1 | killed |
| `r798-b.G5_deleted_on_purpose_outranks_held` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 316 | 1 | killed |
| `r798-b.G6_a_released_hold_the_library_owns_is_dropped` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 316 | 1 | killed |
| `r798-b.G8_a_standing_hold_counts_for_the_canary` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 316 | 1 | killed |
| `r815-b.S1_a_sweep_keeps_a_withheld_hold` | `src/cratekit/label/sweep.py` | user | 2 file(s) | 214 | 1 | killed |
| `u107-a.S06_queued_also` | `src/cratekit/label/sweep.py` | user | 10 file(s) | 932 | 8 | killed |
| `u217.S1_summary_dropped` | `src/cratekit/label/sweep.py` | user | 2 file(s) | 132 | 3 | killed |
| `u238.M4_beyond_leaves_out_unchecked` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 471 | 19 | killed |
| `u238.M5_window_edge_off_by_one` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 471 | 13 | killed |
| `u238.M6_needle_ignored` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 471 | 1 | killed |
| `u277.M2_no_line_before_the_labels_line` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 2 | killed |
| `u277.M3_another_label_before_no_line` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 12 | killed |
| `u277.M4_canary_answer_ignored` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 17 | killed |
| `u277.M5_only_a_mismatch_is_unconfirmed` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 14 | killed |
| `u277.M6_canary_asked_beside_candidates` | `src/cratekit/label/sweep.py` | maintainer | 4 file(s) | 308 | 1 | killed |
| `u277.M7_standing_hold_not_a_canary` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 1 | killed |
| `u277.M8_past_window_counts_other_labels` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 6 | killed |
| `u277.M9_canary_notes_dropped` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 308 | 5 | killed |
| `u52-item-derivation.A3_label_source_acquires` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 2 | killed |
| `u52-item-derivation.S5_dropped_never_accumulated` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 3 | killed |
| `u52-zero-rows.L5_artist_for_missing_returns_none` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `u52-zero-rows.L6_verifier_missing_returns_stub` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `u52-zero-rows.P1_revoked_tombstones_suppress` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `u52-zero-rows.P2_snapshot_read_eagerly` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `r1091.P10_unkept_screen_dropped` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.P1_store_not_loaded` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 19 | killed |
| `r1091.P2_store_after_listing` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 10 | killed |
| `r1091.P3_no_write_on_a_stop` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 6 | killed |
| `r1091.P4_no_write_at_the_end` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 13 | killed |
| `r1091.P5_gone_not_kept` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 10 | killed |
| `r1091.P6_kept_gone_read_as_release` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 34 | killed |
| `r1091.P7_crawl_digest_over_what_is_left` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.P8_calls_ignore_kept` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.P9_unkept_warning_dropped` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 124 | 2 | killed |
| `r835-b.P2_nothing_confirmed_refused` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.P3_unplayable_track_never_asked_again` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u191.M10_crawl_digest_count` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u191.M11_releases_scope_unmarked` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 1 | killed |
| `u191.M12_empty_releases_plan_makes_folder` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 4 | killed |
| `u191.M13_gone_refused` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 42 | killed |
| `u191.M14_review_item_identity_asked` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u191.M15_nothing_left_said_as_nothing_taken` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M16_recorded_year_unchecked` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 1 | killed |
| `u191.M18_listing_relisted` | `src/cratekit/label/playlists_cli.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u191.M19_unread_listing_accepted` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 134 | 1 | killed |
| `u191.M1_crawl_gate_skipped` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 5 | killed |
| `u191.M2_crawl_declined_crawls` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 1 | killed |
| `u191.M3_crawl_asks_the_build_gate` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 5 | killed |
| `u191.M4_threshold_boundary` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M5_threshold_value` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M6_calls_per_release_coefficient` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 5 | killed |
| `u191.M8_time_ignores_pace` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M9_pace_not_configured` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u193.M24_crawl_over_ceiling_dropped` | `src/cratekit/label/playlists_cli.py` | user | 5 file(s) | 508 | 2 | killed |
| `u193.M25_crawl_spent_ignored` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u217.S3_playlists_line` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 62 | 1 | killed |
| `u243.L12_suppressed_releases_unjudged` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 140 | 2 | killed |
| `u243.L5_build_adds_a_tombstoned_track` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 140 | 6 | killed |
| `u243.L6_empty_years_kept` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 140 | 2 | killed |
| `r227.C5_favorites_limit_spelled` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 240 | 1 | killed |
| `r228-operator.D11_non_pink_outside` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `r228-operator.D12_missing_pink_queued` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `r228-operator.D4_union_playlist_first` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D5_pink_missing_dropped` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 2 | killed |
| `r228-operator.D6_empty_after_colour` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D7_colour_unread_warned` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `r228-operator.D8_from_colour_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 5 | killed |
| `r228-operator.D9_from_playlist_zero` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 13 | 4 | killed |
| `r424.B1_colored_key` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 240 | 1 | killed |
| `r424.B3_resume_standing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 240 | 3 | killed |
| `r424.B4_warning_copied` | `src/cratekit/favorites/cli.py` | maintainer | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r856-a.F10_concluded_passed` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 1 | killed |
| `r856-a.F11_warning_total` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 2 | killed |
| `r856-a.F1_hearted_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 2 | killed |
| `r856-a.F2_already_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 1 | killed |
| `r856-a.F3_unmatched_count` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 1 | killed |
| `r856-a.F4_listing_dropped` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 2 | killed |
| `r856-a.F5_listing_off_reasons` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 2 | killed |
| `r856-a.F6_no_match_sentence` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 2 | killed |
| `r856-a.F7_names_from_listing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 1 | killed |
| `r856-a.F8_item_listing` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 1 | killed |
| `r856-a.F9_item_reason_carried` | `src/cratekit/favorites/cli.py` | user | 2 file(s) | 180 | 1 | killed |
| `u51-item-derivation.A1b_colour_writer_passed` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 125 | 1 | killed |
| `u51-item-derivation.H2_hearts_item_not_payload` | `src/cratekit/favorites/cli.py` | user | 1 file(s) | 125 | 14 | killed |
| `u117-operator.D10_no_folder_refusal` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u117-operator.D11_part_way_named` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 2 | killed |
| `u117-operator.D12_move_into_folder` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 8 | killed |
| `u117-operator.D15_playable_only` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u117-operator.D16_recorded_before_move` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u117-operator.D1_heard_left_out` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u117-operator.D2_unsettled_taken` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u117-operator.D4_local_day` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 5 | killed |
| `u117-operator.D5_reuse_by_name` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 5 | killed |
| `u117-operator.D6_reuse_adds_only_missing` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 4 | killed |
| `u117-operator.D7_ambiguous` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u117-operator.D8_age_bound` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 2 | killed |
| `u117-operator.D9_age_configured` | `src/cratekit/label/dated.py` | user | 1 file(s) | 22 | 1 | killed |
| `u123.D1_dated_create_vouched` | `src/cratekit/label/dated.py` | user | 2 file(s) | 60 | 13 | killed |
| `u191.M21_unsettled_answers_read` | `src/cratekit/label/dated.py` | user | 3 file(s) | 146 | 2 | killed |
| `u100-a.H1a_rejected_adopted` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 2 | killed |
| `u100-a.H1b_open_adopted` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 2 | killed |
| `u100-a.H2_kind_filter` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 1 | killed |
| `u100-a.H3_resolved_excluded` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 11 | killed |
| `u100-a.H4_nameless_dropped` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 1 | killed |
| `u237.M1_bare_letter_is_a_mark_again` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 33 | killed |
| `u237.M2_symbol_marks_dropped` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 36 | killed |
| `u237.M3_one_mark_only` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 12 | killed |
| `u237.M4_case_sensitive_mark` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 12 | killed |
| `u237.M5_bare_year_is_a_label` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 4 | killed |
| `u237.M9_year_eats_the_next_digit` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 1 | killed |
| `u252.L7_seam_drops_keywords` | `src/cratekit/label/harvest.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `r382.M16_parser_moved_lowercase` | `src/cratekit/label/catalogue.py` | maintainer | 10 file(s) | 891 | 2 | killed |
| `r515-operator.S1_of_takes_bool` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S2_of_takes_non_int` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S4_of_short_at_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S5_of_short_over_count` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r515-operator.S6_cache_drops_short` | `src/cratekit/label/catalogue.py` | user | 1 file(s) | 94 | 1 | killed |
| `r815-a.G2_forgetting_keeps_the_failure_count` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 214 | 2 | killed |
| `r840-c.C4_no_name_is_the_empty_string` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 354 | 2 | killed |
| `u62.C2_outage_as_credential` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 544 | 4 | killed |
| `u97-b.B3_label_path_raises_the_other_token` | `src/cratekit/label/catalogue.py` | user | 3 file(s) | 1588 | 1 | killed |
| `u237.M10_empty_sides_match` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 2 | killed |
| `u237.M6_substring_again` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 9 | killed |
| `u237.M7_left_word_boundary_only` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 7 | killed |
| `u237.M8_one_direction_only` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 1 | killed |
| `u240.M24_ascii_fold` | `src/cratekit/label/verify.py` | user | 3 file(s) | 404 | 2 | killed |
| `u145.V1_gate_on_nothing` | `src/cratekit/favorites/split_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u145.V2_no_ack` | `src/cratekit/favorites/split_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u120.V1_no_ack` | `src/cratekit/favorites/backfill_cli.py` | user | 1 file(s) | 31 | 1 | killed |
| `r836-g.C1_holds_judged_again` | `src/cratekit/label/prune_cli.py` | user | 5 file(s) | 404 | 1 | killed |

## Zero rows and what they owe

- `r259.O1_no_tracks_guard` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r259.O5_memo` (maintainer facing): maintainer facing, composite not required
- `u193.M25_crawl_spent_ignored` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r424.B4_warning_copied` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `r1634.M10_basis_always_line`

list_for_label, every drop a mismatch: say the answer came from the release's own line even for a lineless one the provider read

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M10_basis_always_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_every_drop_a_mismatch_over_a_held_release_with_no_line_says_the_provider_was_read`

Old text:

```
            basis = READ_LINE if lined else READ_PROVIDER
```

New text:

```
            basis = READ_LINE
```

### `r1634.M13_rereader_unguarded`

LabelSource._rereader: hand the forced read over bare, so a provider failure on it ends internal-error

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M13_rereader_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_sync.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary`

Old text:

```
        return _guarded(lambda claimed, release: catalogue.reread_release(claimed, release))
```

New text:

```
        return lambda claimed, release: catalogue.reread_release(claimed, release)
```

### `r1634.M14_rereader_beside_a_bare_verifier`

LabelSource._rereader: take the catalogue's forced read though a bare verifier was handed in

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M14_rereader_beside_a_bare_verifier`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`

Old text:

```
        if self.verify is not None or self.catalogue is None:
            return None
```

New text:

```
        if self.catalogue is None:
            return None
```

### `r1634.M15_how_reworded`

Canary.how: the provider basis no longer says the provider was read

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M15_how_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`
- Collected: 213 against a baseline of 213
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
    READ_PROVIDER: "read again from the provider",
```

New text:

```
    READ_PROVIDER: "verified once more",
```

### `r1634.M18_basis_not_in_detail`

Canary.to_json: the worker's detail no longer carries the basis

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M18_basis_not_in_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
            "basis": self.basis,
```

New text:

```
            "basis": "",
```

### `r1634.M19_another_act_replaces_a_gone_one`

list_for_label: a gone answer's second read may go to a held release whose line names another act, which answers mismatch and names that act as the needle

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M19_another_act_replaces_a_gone_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`

Old text:

```
                one for one in order[1:] if line_reading(one, claimed) != LINE_NAMES_OTHER
```

New text:

```
                one for one in order[1:] if True
```

### `r1634.M1_mismatch_mode_always`

list_for_label: read every listing as all mismatches, so a drop with no credit asks the ordinary verifier, which judges a held label line from its line (the defect)

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M1_mismatch_mode_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`

Old text:

```
        if _answered_by_name(dropped):
            answered = label_verify.verify_release(claimed, chosen, search=verify)
```

New text:

```
        if True:
            answered = label_verify.verify_release(claimed, chosen, search=verify)
```

### `r1634.M20_in_place_note_dropped`

list_for_label: a release read in a gone one's place no longer says so, so a refusal tells two reads as one

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M20_in_place_note_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
                        f"read in place of release {first}, which the provider no longer has",
```

New text:

```
                        "",
```

### `r1634.M2_mismatch_mode_never`

list_for_label: never take the ordinary verifier, so every drop a mismatch forces a provider read it did not need

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M2_mismatch_mode_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_four_held_releases_whose_line_is_the_label_answer_nothing_new`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_canary_is_a_held_release_whose_line_the_needle_confirms`
  - `tests/test_label_canary.py::test_the_forced_read_is_asked_only_when_a_drop_is_not_a_mismatch`
  - `tests/test_label_canary.py::test_the_live_shape_answers_nothing_new_rather_than_refusing`
  - `tests/test_label_canary.py::test_the_record_names_the_release_re_verified_and_what_it_answered`
  - `tests/test_label_canary.py::test_the_worker_answers_the_live_shape_as_nothing_new`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`
  - `tests/test_label_canary.py::test_with_every_drop_a_mismatch_a_held_labels_line_is_asked_before_one_with_none`
  - `tests/test_label_canary.py::test_with_every_held_line_naming_another_act_the_newest_is_asked_and_all_count`

Old text:

```
        if _answered_by_name(dropped):
            answered = label_verify.verify_release(claimed, chosen, search=verify)
```

New text:

```
        if False:
            answered = label_verify.verify_release(claimed, chosen, search=verify)
```

### `r1634.M3_forced_read_dropped`

list_for_label: never take the forced read, so a lined held release counts as unverified and a real nothing new refuses

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M3_forced_read_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_forced_read_that_raises_fails_the_item_in_the_lookup_vocabulary`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`

Old text:

```
        elif reread is not None:
```

New text:

```
        elif False:
```

### `r1634.M4_no_read_confirms`

list_for_label, no forced read to hand: count a lined held release confirmed rather than unverified

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M4_no_read_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`

Old text:

```
            answered = {"verdict": "unconfirmed", "notes": "no provider read"}
```

New text:

```
            answered = {"verdict": "confirmed", "notes": "no provider read"}
```

### `r1634.M5_no_read_asks_the_line`

list_for_label, no forced read to hand: ask the ordinary verifier for a lined held release, which judges it from its line

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M5_no_read_asks_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`

Old text:

```
        elif not lined:
```

New text:

```
        elif True:
```

### `r1634.M6_gone_not_passed_over`

list_for_label: a gone answer stands, so a withdrawn held release a kept listing still lists refuses a healthy label

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M6_gone_not_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
            if answered.get("verdict") == RELEASE_GONE and following:
```

New text:

```
            if False and following:
```

### `r1634.M7_any_answer_passed_over`

list_for_label: pass over any answer that is not confirmed, so a degraded provider gets a second read and the cap is spent on every refusal

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M7_any_answer_passed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`

Old text:

```
            if answered.get("verdict") == RELEASE_GONE and following:
```

New text:

```
            if answered.get("verdict") != "confirmed" and following:
```

### `r1634.M8_order_label_line_first`

_canary_order, a drop with no credit: rank a held label line ahead of a lineless one (U277's lineless preference lost)

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M8_order_label_line_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked`

Old text:

```
        return reading != LINE_ABSENT, reading
```

New text:

```
        return False, reading
```

### `r1634.M9_order_other_act_before_label`

_canary_order, a drop with no credit: rank another act's held line ahead of the label's, so a healthy read of a RAWAXXX hold refuses (R-1635)

- File: `src/cratekit/label/sweep.py`
- Source: `r1634.json`, row `M9_order_other_act_before_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 390 against a baseline of 390
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`

Old text:

```
        return reading != LINE_ABSENT, reading
```

New text:

```
        return reading != LINE_ABSENT, -reading
```

### `r259-b.O2_unreadable_row`

A release with a row the reader cannot read counts as owned

- File: `src/cratekit/label/sweep.py`
- Source: `r259-b.json`, row `O2_unreadable_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_release_with_a_row_the_reader_cannot_read_is_offered`

Old text:

```
        except match.UnreadableList:
            return False
```

New text:

```
        except match.UnreadableList:
            return True
```

### `r259.L2_library_kwarg`

OwnedReleases ignores the library it is handed and walks its own

- File: `src/cratekit/label/sweep.py`
- Source: `r259.json`, row `L2_library_kwarg`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_of_two_labels_walks_the_library_once`

Old text:

```
            if self._library_of is not None:
```

New text:

```
            if False:
```

### `r259.O1_no_tracks_guard`

A release the provider lists with no track reads as owned, since all over nothing is True

- File: `src/cratekit/label/sweep.py`
- Source: `r259.json`, row `O1_no_tracks_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not rows:
            return False

```

New text:

```
(empty)
```

### `r259.O5_memo`

The answer is not kept, so the increment's scope reads every release a second time

- File: `src/cratekit/label/sweep.py`
- Source: `r259.json`, row `O5_memo`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if identity not in self._answers:
            self._answers[identity] = self._holds(identity)
        return self._answers[identity]
```

New text:

```
        return self._holds(identity)
```

### `r261.S1_roster_unread_read`

_crawl_or_refuse ignores the unread a roster carries

- File: `src/cratekit/label/sweep.py`
- Source: `r261.json`, row `S1_roster_unread_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        built = tuple(getattr(artist, "unread", None) or ())
```

New text:

```
        built = ()
```

### `r261.S2_own_missing`

_crawl_or_refuse drops the methods a plain artist object lacks

- File: `src/cratekit/label/sweep.py`
- Source: `r261.json`, row `S2_own_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_plain_artist_object_missing_one_listing_is_recorded_by_the_source`

Old text:

```
    return releases, (*built, *(missing_listing(artist, method) for method in skipped))
```

New text:

```
    return releases, built
```

### `r261.S3_source_collects`

LabelSource.list_recent does not carry a label's unread onto the source

- File: `src/cratekit/label/sweep.py`
- Source: `r261.json`, row `S3_source_collects`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_plain_artist_object_missing_one_listing_is_recorded_by_the_source`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
            unread.extend(listing.unread)
```

New text:

```
            pass
```

### `r261.S4_existing_can_list`

Sample of an existing guard: _crawl_or_refuse accepts an object exposing no listing at all

- File: `src/cratekit/label/sweep.py`
- Source: `r261.json`, row `S4_existing_can_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing`

Old text:

```
    if not listable:
```

New text:

```
    if False:
```

### `r704-a.S1_no_cause_chain_check`

the sweep never asks whether the error or its declared causes are a rate limit, so the sitting's TooManyRequests is permanent again

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S1_no_cause_chain_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_resumed_job_rearms_the_rate_limited_label_and_not_the_settled_one`

Old text:

```
    if any(is_rate_limit(link) for link in _linked(exc, "__cause__")):
        return run.LookupFailure(message, rate_limited=True)

```

New text:

```
(empty)
```

### `r704-a.S2_cause_walk_reads_only_the_error`

the declared cause chain is not walked, so a client error raised from a TooManyRequests reads as permanent

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S2_cause_walk_reads_only_the_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(is_rate_limit(link) for link in _linked(exc, "__cause__")):
```

New text:

```
    if any(is_rate_limit(link) for link in (exc,)):
```

### `r704-a.S3_no_context_status_check`

a non JSON 429 whose status sits only in the implicit context is read as permanent

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S3_no_context_status_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
        return run.LookupFailure(message, rate_limited=True)

```

New text:

```
(empty)
```

### `r704-a.S4_context_walk_one_level`

the context walk stops one level down, above the 429 the client's translation leaves two contexts deep

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S4_context_walk_one_level`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
```

New text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in (exc, exc.__context__)):
```

### `r704-a.S5_context_read_by_type`

an implicit context is read by its type as well as its status, so an unrelated error raised while handling a rate limit is called one

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S5_context_read_by_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
```

New text:

```
    if any(is_rate_limit(link) for link in _linked(exc, "__context__")):
```

### `r704-a.S6_status_coefficient`

the context check asks for a 503 rather than the rate limit statuses

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S6_status_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
```

New text:

```
    if any(status_of(link) in {503} for link in _linked(exc, "__context__")):
```

### `r704-a.S7_probe_unclassified`

the listing probe boundary hands the classifier a plain error, so a rate limit on a lazy listing attribute is permanent

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S7_probe_unclassified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`

Old text:

```
            f"that is not an empty catalogue",
            exc,
        ) from exc
    if not listable:
```

New text:

```
            f"that is not an empty catalogue",
            RuntimeError(),
        ) from exc
    if not listable:
```

### `r704-a.S8_crawl_unclassified`

the crawl boundary hands the classifier a plain error, the listing's spent ladder is permanent again

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S8_crawl_unclassified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_resumed_job_rearms_the_rate_limited_label_and_not_the_settled_one`

Old text:

```
            f"({type(exc).__name__}: {exc}); that is not an empty catalogue",
            exc,
        ) from exc
```

New text:

```
            f"({type(exc).__name__}: {exc}); that is not an empty catalogue",
            RuntimeError(),
        ) from exc
```

### `r704-a.S9_resolve_unclassified`

the artist resolve boundary hands the classifier a plain error

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S9_resolve_unclassified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`

Old text:

```
                    f"were never listed",
                    exc,
                ) from exc
```

New text:

```
                    f"were never listed",
                    RuntimeError(),
                ) from exc
```

### `r790-a.S2_held_is_not_refiled`

list_for_label: drop the held check, so a release already in the queue is verified and filed again

- File: `src/cratekit/label/sweep.py`
- Source: `r790-a.json`, row `S2_held_is_not_refiled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_held_release_since_downloaded_keeps_its_place`
  - `tests/test_label_offer_window.py::test_a_later_sweep_asks_the_provider_nothing_about_releases_it_already_holds`
  - `tests/test_label_offer_window.py::test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again`

Old text:

```
        if identity in offered_ids:
            held += 1
```

New text:

```
        if False:
            held += 1
```

### `r790-a.S4_default_is_the_offer`

list_for_label: default the window to the track limit again, the four hundred R-790 is about

- File: `src/cratekit/label/sweep.py`
- Source: `r790-a.json`, row `S4_default_is_the_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`
  - `tests/test_label_offer_window.py::test_the_window_defaults_to_the_configuration_and_the_entry_overrides_it`

Old text:

```
        else registry.effective_offer(entry, cfg.labels.offer_per_sweep)
```

New text:

```
        else registry.effective_limit(entry)
```

### `r790-b.S7_first_run_kept`

offer_release: stamp the latest run over the one that filed the item

- File: `src/cratekit/label/sweep.py`
- Source: `r790-b.json`, row `S7_first_run_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_first_run_stays_the_filing_run_when_an_open_item_is_offered_again`

Old text:

```
        payload[SWEEP_RUN] = held_run or run_id
```

New text:

```
        payload[SWEEP_RUN] = run_id
```

### `r798-b.G3_a_held_release_takes_a_place`

list_for_label: stop counting a held release toward the offer window, so a label of another label's music is read to the end of its catalogue

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G3_a_held_release_takes_a_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_held_release_and_a_queued_one_both_take_a_place`
  - `tests/test_label_genre_gate.py::test_a_sweep_that_holds_some_releases_files_no_more_than_the_window`

Old text:

```
        if held + len(gated) + len(candidates) >= cap:
```

New text:

```
        if held + len(candidates) >= cap:
```

### `r798-b.G4_a_returned_hold_is_never_judged`

list_for_label: judge a hold a person returned like any standing hold, so a release they asked for is held again

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G4_a_returned_hold_is_never_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_returned_hold_the_queue_does_not_hold_is_filed_and_never_judged`

Old text:

```
        if standing is not None and standing.state == review.HOLD_RETURNED:
```

New text:

```
        if False:
```

### `r798-b.G5_deleted_on_purpose_outranks_held`

list_for_label: keep the hold on a release tombstoned since, so it stays counted as held

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G5_deleted_on_purpose_outranks_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_held_release_deleted_on_purpose_since_is_held_no_longer`

Old text:

```
            if was is not None and was.state == review.HOLD_HELD:
```

New text:

```
            if False:
```

### `r798-b.G6_a_released_hold_the_library_owns_is_dropped`

list_for_label: file a released hold without asking whether the library came to own it

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G6_a_released_hold_the_library_owns_is_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_released_hold_the_library_came_to_own_is_dropped_and_not_filed`

Old text:

```
            elif identity in owned_ids:
```

New text:

```
            elif False:
```

### `r798-b.G8_a_standing_hold_counts_for_the_canary`

list_for_label: leave standing holds out of the releases a dead verifier could not confirm again, so a window of holds hides one

- File: `src/cratekit/label/sweep.py`
- Source: `r798-b.json`, row `G8_a_standing_hold_counts_for_the_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`, `tests/test_label_offer_window.py`, `tests/test_label_workers.py`
- Collected: 316 against a baseline of 316
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dead_verifier_over_a_window_of_standing_holds_refuses`

Old text:

```
            held_unconfirmed = held + sum(1 for one in gated if one.standing)
```

New text:

```
            held_unconfirmed = held
```

### `r815-b.S1_a_sweep_keeps_a_withheld_hold`

list_for_label: drop a withheld hold the window does not reach, as any other

- File: `src/cratekit/label/sweep.py`
- Source: `r815-b.json`, row `S1_a_sweep_keeps_a_withheld_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_withheld_release_the_window_does_not_reach_is_not_dropped_when_its_kind_changes`

Old text:

```
            if standing.payload.get(review.WITHHELD_FIELD):
                continue
```

New text:

```
            if False:
                continue
```

### `u107-a.S06_queued_also`

sweep.QueuedReleases: ignore the second container, so an asked release takes no place in the offer window

- File: `src/cratekit/label/sweep.py`
- Source: `u107-a.json`, row `S06_queued_also`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_genre_gate.py`, `tests/test_label_judge.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 932 against a baseline of 932
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
        if self.also is not None and identity in self.also:
```

New text:

```
        if False:
```

### `u217.S1_summary_dropped`

kept_of: never carry the roster's summary onto the sweep's listing

- File: `src/cratekit/label/sweep.py`
- Source: `u217.json`, row `S1_summary_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_sync.py`
- Collected: 132 against a baseline of 132
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`

Old text:

```
    return held if isinstance(held, kept_listing.Summary) else None
```

New text:

```
    return None
```

### `u238.M4_beyond_leaves_out_unchecked`

list_for_label: beyond is the label's own only, so the recorded round drops every unchecked release

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M4_beyond_leaves_out_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`, `tests/test_label_judge.py`
- Collected: 471 against a baseline of 471
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again`
  - `tests/test_label_offer_window.py::test_a_release_with_no_copyright_line_is_unchecked_never_dropped`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_tombstoned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones`
  - `tests/test_label_offer_window.py::test_an_owned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        beyond=own_past + unchecked_past,
```

New text:

```
        beyond=own_past,
```

### `u238.M5_window_edge_off_by_one`

list_for_label: start the count one release past the window's edge

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M5_window_edge_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`, `tests/test_label_judge.py`
- Collected: 471 against a baseline of 471
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_release_already_in_the_queue_holds_a_place_and_is_not_verified_again`
  - `tests/test_label_offer_window.py::test_a_release_with_no_copyright_line_is_unchecked_never_dropped`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_tombstoned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_a_watermark_past_every_release_still_offers_the_unowned_unoffered_ones`
  - `tests/test_label_offer_window.py::test_an_owned_release_takes_no_place_in_the_window`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`

Old text:

```
    own_past, unchecked_past = _past_window(listed[examined:], claimed)
```

New text:

```
    own_past, unchecked_past = _past_window(listed[examined + 1:], claimed)
```

### `u238.M6_needle_ignored`

list_for_label: judge the lines past the window by the label's name, not its --match needle

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M6_needle_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`, `tests/test_label_judge.py`
- Collected: 471 against a baseline of 471
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`

Old text:

```
    own_past, unchecked_past = _past_window(listed[examined:], claimed)
```

New text:

```
    own_past, unchecked_past = _past_window(listed[examined:], entry.name)
```

### `u277.M2_no_line_before_the_labels_line`

line_reading order: rank a held release with no line ahead of one whose line names the label

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M2_no_line_before_the_labels_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_with_every_drop_a_mismatch_a_held_labels_line_is_asked_before_one_with_none`

Old text:

```
LINE_NAMES_LABEL = 0
LINE_ABSENT = 1
```

New text:

```
LINE_NAMES_LABEL = 1
LINE_ABSENT = 0
```

### `u277.M3_another_label_before_no_line`

line_reading order: rank a held release whose line names another label ahead of one with no line

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M3_another_label_before_no_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_every_drop_a_mismatch_over_a_held_release_with_no_line_says_the_provider_was_read`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`
  - `tests/test_label_canary.py::test_with_no_held_line_naming_the_label_a_held_release_with_no_line_comes_next`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked`
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`

Old text:

```
LINE_NAMES_OTHER = 2
```

New text:

```
LINE_NAMES_OTHER = 1
```

### `u277.M4_canary_answer_ignored`

list_for_label: never count the held releases unconfirmed, whatever the canary answered, so a dead verifier reads as nothing new

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M4_canary_answer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 17 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked`
  - `tests/test_label_canary.py::test_with_every_held_line_naming_another_act_the_newest_is_asked_and_all_count`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if not canary.confirmed:
            held_unconfirmed
```

New text:

```
        if False:
            held_unconfirmed
```

### `u277.M5_only_a_mismatch_is_unconfirmed`

Canary.confirmed: read anything but a mismatch as confirmed, so an unconfirmed answer from a dead verifier passes

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M5_only_a_mismatch_is_unconfirmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 14 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_source_handed_a_bare_verifier_beside_a_catalogue_forces_no_read`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_the_verifier_gave_no_answer_for_a_held_release_with_no_line_is_asked`
  - `tests/test_label_canary.py::test_with_no_provider_read_to_hand_a_held_line_counts_as_unverified`
  - `tests/test_label_genre_gate.py::test_a_dead_verifier_over_a_window_of_standing_holds_refuses`
  - `tests/test_label_offer_window.py::test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new`

Old text:

```
        return self.verdict == "confirmed"
```

New text:

```
        return self.verdict != "mismatch"
```

### `u277.M6_canary_asked_beside_candidates`

list_for_label: ask the canary even when the sweep confirmed a candidate, one provider call a sweep more

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M6_canary_asked_beside_candidates`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_canary.py::test_no_canary_is_asked_when_the_sweep_confirmed_something`

Old text:

```
    if held_releases and dropped and not candidates:
```

New text:

```
    if held_releases and dropped:
```

### `u277.M7_standing_hold_not_a_canary`

list_for_label: leave a standing genre gate hold out of the releases the canary is chosen from

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M7_standing_hold_not_a_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dead_verifier_over_a_window_of_standing_holds_refuses`

Old text:

```
                gated.append(Gated(_candidate(entry, release), again, standing=True))
                held_releases.append(release)
```

New text:

```
                gated.append(Gated(_candidate(entry, release), again, standing=True))
```

### `u277.M8_past_window_counts_other_labels`

_past_window: count a release whose line names another label as the label's own past the window (the shared reading, U238)

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M8_past_window_counts_other_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_past_the_window_counts_only_the_labels_own_releases_and_the_unchecked`
  - `tests/test_label_offer_window.py::test_the_count_past_the_window_uses_the_labels_match_needle`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`
  - `tests/test_label_sync.py::test_nothing_new_after_an_answer_says_the_count_past_the_window`

Old text:

```
        elif reading == LINE_NAMES_LABEL:
            own += 1
```

New text:

```
        else:
            own += 1
```

### `u277.M9_canary_notes_dropped`

list_for_label: keep the canary's verdict and lose its notes, so a mismatch no longer says whom the release is credited to

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M9_canary_notes_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 308 against a baseline of 308
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
            notes=str(answered.get("notes") or ""),
```

New text:

```
            notes="",
```

### `u52-item-derivation.A3_label_source_acquires`

Declare the labels source an acquiring one, which is the state R-140 was recorded against

- File: `src/cratekit/label/sweep.py`
- Source: `u52-item-derivation.json`, row `A3_label_source_acquires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_source_declares_that_it_does_not_acquire`
  - `tests/test_incremental_sync.py::test_the_labels_spec_agrees_with_the_source_that_offers`

Old text:

```
    acquires = False
```

New text:

```
    acquires = True
```

### `u52-item-derivation.S5_dropped_never_accumulated`

Stop accumulating the dropped population in LabelSource.list_recent, so the refusal above can never see one

- File: `src/cratekit/label/sweep.py`
- Source: `u52-item-derivation.json`, row `S5_dropped_never_accumulated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_that_confirmed_none_of_what_it_read_fails_rather_than_succeeding`
  - `tests/test_label_workers.py::test_a_sweep_that_read_releases_and_confirmed_none_of_them_still_refuses`
  - `tests/test_label_workers.py::test_the_unconfirmed_refusal_says_how_many_were_read_and_that_the_provider_answered`

Old text:

```
            discarded.extend(listing.dropped)
```

New text:

```
            pass
```

### `u52-zero-rows.L5_artist_for_missing_returns_none`

The bare skip R-135 named in miniature: a label with no catalogue object at all returns None rather than refusing

- File: `src/cratekit/label/sweep.py`
- Source: `u52-zero-rows.json`, row `L5_artist_for_missing_returns_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_missing_artist_refusal_names_the_missing_object_not_the_listing`

Old text:

```
        raise run.LookupFailure(
            f"no catalogue object was available for the registered label "
            f"{entry.name!r}, so its releases were never listed; that is not "
            f"a label with nothing new"
        )
```

New text:

```
        return None
```

### `u52-zero-rows.L6_verifier_missing_returns_stub`

A source built with neither verifier nor catalogue confirms nothing instead of refusing, so every release is dropped as unconfirmed

- File: `src/cratekit/label/sweep.py`
- Source: `u52-zero-rows.json`, row `L6_verifier_missing_returns_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_source_with_neither_verifier_nor_catalogue_refuses_rather_than_confirming_nothing`

Old text:

```
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )
```

New text:

```
        def unconfirmed(claimed: str, release: Any) -> Mapping[str, Any]:
            return {}

        return unconfirmed
```

### `u52-zero-rows.P1_revoked_tombstones_suppress`

Snapshot revoked tombstones too, so a lifted suppression silently keeps a release out of the review queue

- File: `src/cratekit/label/sweep.py`
- Source: `u52-zero-rows.json`, row `P1_revoked_tombstones_suppress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_revoked_tombstone_no_longer_keeps_a_release_out_of_the_queue`

Old text:

```
            snapshot = {record.suppression_id for record in store.suppressions()}
```

New text:

```
            snapshot = {
                record.suppression_id
                for record in store.suppressions(include_revoked=True)
            }
```

### `u52-zero-rows.P2_snapshot_read_eagerly`

THE LAZY READ: take the snapshot when the reader is built, which fires the unreadable store refusal on a label that has no confirmed release to ask about

- File: `src/cratekit/label/sweep.py`
- Source: `u52-zero-rows.json`, row `P2_snapshot_read_eagerly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_unreadable_tombstone_store_does_not_fail_a_label_with_nothing_to_ask`

Old text:

```
    snapshot: set[str] | None = None
```

New text:

```
    snapshot: set[str] | None = {
        record.suppression_id
        for record in DecisionStore(tombstone.STORE_KEY, cfg).suppressions()
    }
```

### `r1091.P10_unkept_screen_dropped`

_reads_said: say the reads are kept on the build gate's screen when they could not be written

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P10_unkept_screen_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`

Old text:

```
        if reads.unkept:
            return f"all {reads.read_now} release read(s) made by this run; {_unkept_said(reads)}"
```

New text:

```
        if False:
            return f"all {reads.read_now} release read(s) made by this run; {_unkept_said(reads)}"
```

### `r1091.P1_store_not_loaded`

label_playlists: hand the full build no store, so every run reads the whole catalogue again

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P1_store_not_loaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_build_refused_part_way_by_a_failed_read_keeps_the_reads_before_it`
  - `tests/test_label_playlists_kept.py::test_a_crawl_answered_build_reads_each_release_once_over_its_three_runs`
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_first_build_says_its_reads_are_kept_for_the_apply_run`
  - `tests/test_label_playlists_kept.py::test_a_gone_release_is_kept_as_gone_and_counted_without_asking_again`
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year`
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_resume_under_the_same_crawl_answer_is_not_stale`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - ... and 4 more, see the JSON sidecar

Old text:

```
            read = read_catalogue(cfg, entry, found, listed=listed, reads=reads)
```

New text:

```
            read = read_catalogue(cfg, entry, found, listed=listed, reads=None)
```

### `r1091.P2_store_after_listing`

label_playlists: load the store after the listing, so an unusable store refuses after the listing's calls

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P2_store_after_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[[]-the document is a list, not a map]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written6-is malformed]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written7-carries the year]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written8-says gone]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written9-carries the year]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "another", "reads": {}}-it names the label]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "kompakt", "reads": []}-its reads are not a map]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "kompakt", "reads": {"r1": {"year": 2021, "tracks": []}}}-carries no instant]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 99, "label_id": "kompakt", "reads": {}}-it says version 99]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{not json-it is not JSON]`

Old text:

```
            reads = kept_reads.KeptReads.load(entry.label_id)
            listed = list_catalogue(cfg, entry, found)
```

New text:

```
            listed = list_catalogue(cfg, entry, found)
            reads = kept_reads.KeptReads.load(entry.label_id)
```

### `r1091.P3_no_write_on_a_stop`

_grouped: write nothing when the read stops, so a parked build keeps nothing

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P3_no_write_on_a_stop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_build_refused_part_way_by_a_failed_read_keeps_the_reads_before_it`
  - `tests/test_label_playlists_kept.py::test_a_resume_under_the_same_crawl_answer_is_not_stale`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_the_build_gate_counts_the_calls_left_after_the_kept_reads`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
        try:
            reads.flush()
        except Exception as lost:
```

New text:

```
        try:
            pass
        except Exception as lost:
```

### `r1091.P4_no_write_at_the_end`

_grouped: write nothing after a clean read, so the apply run reads the catalogue again

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P4_no_write_at_the_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_crawl_answered_build_reads_each_release_once_over_its_three_runs`
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_gone_release_is_kept_as_gone_and_counted_without_asking_again`
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year`
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_an_abort_after_a_failed_write_still_warns_the_reads_were_not_kept`
  - `tests/test_label_playlists_kept.py::test_the_gate_run_and_the_apply_run_read_each_release_once`

Old text:

```
        raise
    reads.flush()
    return grouped
```

New text:

```
        raise
    return grouped
```

### `r1091.P5_gone_not_kept`

_read_one: keep no answer that a release is gone, so it is asked again every run

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P5_gone_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_crawl_answered_build_reads_each_release_once_over_its_three_runs`
  - `tests/test_label_playlists_kept.py::test_a_first_build_says_its_reads_are_kept_for_the_apply_run`
  - `tests/test_label_playlists_kept.py::test_a_gone_release_is_kept_as_gone_and_counted_without_asking_again`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_the_gate_run_and_the_apply_run_read_each_release_once`

Old text:

```
            reads.keep_gone(release_id)
```

New text:

```
            pass
```

### `r1091.P6_kept_gone_read_as_release`

_read_one: answer a kept gone release as a release with no tracks, so it is counted undated rather than gone

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P6_kept_gone_read_as_release`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - ... and 19 more, see the JSON sidecar

Old text:

```
        return None if held.gone else (held.tracks, held.year)
```

New text:

```
        return (held.tracks, held.year)
```

### `r1091.P7_crawl_digest_over_what_is_left`

Estimate.plan: digest the releases left to read, so a resume under the same crawl answer is stale

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P7_crawl_digest_over_what_is_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_resume_under_the_same_crawl_answer_is_not_stale`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
                {"kind": CRAWL_GATE, "label": self.label_id, "releases": self.releases}
```

New text:

```
                {"kind": CRAWL_GATE, "label": self.label_id, "releases": self.releases - self.kept}
```

### `r1091.P8_calls_ignore_kept`

Estimate.calls: count every listed release, so a resumed build asks the crawl gate over reads it will not make

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P8_calls_ignore_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_the_build_gate_counts_the_calls_left_after_the_kept_reads`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
        return (self.releases - self.kept) * CALLS_PER_RELEASE
```

New text:

```
        return self.releases * CALLS_PER_RELEASE
```

### `r1091.P9_unkept_warning_dropped`

_unkept_warnings: say nothing on the run's warnings when the reads could not be written

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P9_unkept_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_an_abort_after_a_failed_write_still_warns_the_reads_were_not_kept`

Old text:

```
    if reads is None or not reads.unkept:
        return []
```

New text:

```
    if True:
        return []
```

### `r835-b.P2_nothing_confirmed_refused`

playlists_cli.read_catalogue: a catalogue that confirmed none of its releases is shown as an empty label

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r835-b.json`, row `P2_nothing_confirmed_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_catalogue_that_confirms_nothing_is_refused_not_shown_empty`

Old text:

```
    if confirmed.dropped and not confirmed.releases:
```

New text:

```
    if False:
```

### `r835-c.P3_unplayable_track_never_asked_again`

playlists_cli.read_catalogue: a track the provider will not play is asked for and refused on every run

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r835-c.json`, row `P3_unplayable_track_never_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_play_is_never_planned`

Old text:

```
            if identifier and getattr(row, "available", True) is not False:
```

New text:

```
            if identifier:
```

### `u191.M10_crawl_digest_count`

Estimate.plan: drop the release count from the crawl digest, so an answer outlives a grown listing

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M10_crawl_digest_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_the_crawl_gate_is_asked_again_when_the_listing_grows`

Old text:

```
                {"kind": CRAWL_GATE, "label": self.label_id, "releases": self.releases}
```

New text:

```
                {"kind": CRAWL_GATE, "label": self.label_id}
```

### `u191.M11_releases_scope_unmarked`

_payload: never mark a releases plan, so a full build's answer approves it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M11_releases_scope_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_an_answer_given_to_a_full_build_is_not_taken_for_a_releases_build`

Old text:

```
    if scope:
```

New text:

```
    if False:
```

### `u191.M12_empty_releases_plan_makes_folder`

label_playlists: plan the account even when no taken release has a year, so an empty folder is made

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M12_empty_releases_plan_makes_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_go_whose_every_release_is_gone_says_so_and_not_that_nothing_was_taken`
  - `tests/test_label_playlists_releases.py::test_a_recorded_year_that_is_not_four_digits_is_undated`
  - `tests/test_label_playlists_releases.py::test_an_answer_no_go_has_taken_is_not_read`
  - `tests/test_label_playlists_releases.py::test_another_labels_answers_are_not_read`

Old text:

```
        if not (from_releases and not read.years):
```

New text:

```
        if True:
```

### `u191.M13_gone_refused`

_grouped: refuse the plan over a release the provider no longer has, instead of counting it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M13_gone_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 42 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_renamed_label_is_a_different_plan_and_its_approval_is_stale`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - ... and 27 more, see the JSON sidecar

Old text:

```
            gone += 1
            continue
```

New text:

```
            raise incomplete(entry, "gone")
```

### `u191.M14_review_item_identity_asked`

_unnamed: treat an item identity as a release, so the provider is asked for it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M14_review_item_identity_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_release_named_only_by_its_review_item_is_never_asked_for_or_shown_as_read`

Old text:

```
    return not identity or identity.startswith("item:")
```

New text:

```
    return not identity
```

### `u191.M15_nothing_left_said_as_nothing_taken`

label_playlists: warn that nothing was taken when a go took releases and all were gone

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M15_nothing_left_said_as_nothing_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_go_whose_every_release_is_gone_says_so_and_not_that_nothing_was_taken`
  - `tests/test_label_playlists_releases.py::test_a_recorded_year_that_is_not_four_digits_is_undated`

Old text:

```
        elif not taken:
```

New text:

```
        elif True:
```

### `u191.M16_recorded_year_unchecked`

_year: take a recorded year whatever its shape

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M16_recorded_year_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_recorded_year_that_is_not_four_digits_is_undated`

Old text:

```
    return listed if len(listed) == 4 and listed.isdigit() else ""
```

New text:

```
    return listed
```

### `u191.M18_listing_relisted`

read_catalogue: list the label again even when the build already listed it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M18_listing_relisted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_full_build_lists_the_label_once_per_run`

Old text:

```
    if listed is None:
        listed = list_catalogue(cfg, entry, found)
    try:
```

New text:

```
    if True:
        listed = list_catalogue(cfg, entry, found)
    try:
```

### `u191.M19_unread_listing_accepted`

list_catalogue: plan from a listing read in part (existing guard, moved by this unit)

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M19_unread_listing_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`, `tests/test_prune.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_catalogue_read_in_part_is_refused_before_the_gate`

Old text:

```
    if listed.unread:
```

New text:

```
    if False:
```

### `u191.M1_crawl_gate_skipped`

label_playlists: never stop at the crawl gate, so a full build over the threshold reads every release before asking anything

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M1_crawl_gate_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate`
  - `tests/test_label_playlists_releases.py::test_a_full_build_answered_crawl_reads_the_catalogue_and_asks_the_build_gate`
  - `tests/test_label_playlists_releases.py::test_a_full_build_declined_at_its_crawl_gate_reads_and_writes_nothing`
  - `tests/test_label_playlists_releases.py::test_a_full_build_over_the_threshold_stops_at_its_gate_after_the_count`
  - `tests/test_label_playlists_releases.py::test_the_crawl_gate_is_asked_again_when_the_listing_grows`

Old text:

```
            if counted.over:
```

New text:

```
            if False:
```

### `u191.M2_crawl_declined_crawls`

label_playlists: read the catalogue even when the crawl gate is answered abort

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M2_crawl_declined_crawls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_full_build_declined_at_its_crawl_gate_reads_and_writes_nothing`

Old text:

```
                if option != "crawl":
```

New text:

```
                if False:
```

### `u191.M3_crawl_asks_the_build_gate`

label_playlists: ask the build gate where the crawl gate belongs, so one answer covers both

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M3_crawl_asks_the_build_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_playlists.py`
- Collected: 80 against a baseline of 80
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate`
  - `tests/test_label_playlists_releases.py::test_a_full_build_answered_crawl_reads_the_catalogue_and_asks_the_build_gate`
  - `tests/test_label_playlists_releases.py::test_a_full_build_declined_at_its_crawl_gate_reads_and_writes_nothing`
  - `tests/test_label_playlists_releases.py::test_a_full_build_over_the_threshold_stops_at_its_gate_after_the_count`
  - `tests/test_label_playlists_releases.py::test_the_crawl_gate_is_asked_again_when_the_listing_grows`

Old text:

```
                    _gate(ctx, CRAWL_GATE), plan=crawl, context=counted.shown()
```

New text:

```
                    _gate(ctx, BUILD_GATE), plan=crawl, context=counted.shown()
```

### `u191.M4_threshold_boundary`

Estimate.over: stop at the threshold itself rather than over it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M4_threshold_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`

Old text:

```
        return self.calls > FULL_BUILD_CALLS
```

New text:

```
        return self.calls >= FULL_BUILD_CALLS
```

### `u191.M5_threshold_value`

FULL_BUILD_CALLS: a threshold ten times higher, so a label of two thousand releases crawls unasked

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M5_threshold_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`

Old text:

```
FULL_BUILD_CALLS = 500
```

New text:

```
FULL_BUILD_CALLS = 5000
```

### `u191.M6_calls_per_release_coefficient`

CALLS_PER_RELEASE: one call a release, halving every estimate

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M6_calls_per_release_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_full_build_over_the_threshold_stops_at_its_gate_after_the_count`
  - `tests/test_label_playlists_releases.py::test_a_full_build_under_the_threshold_asks_only_the_build_gate`
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`
  - `tests/test_label_playlists_releases.py::test_the_estimate_reads_the_configured_pace`

Old text:

```
CALLS_PER_RELEASE = 2
```

New text:

```
CALLS_PER_RELEASE = 1
```

### `u191.M8_time_ignores_pace`

Estimate.seconds: one second a call whatever the pace

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M8_time_ignores_pace`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`
  - `tests/test_label_playlists_releases.py::test_the_estimate_reads_the_configured_pace`

Old text:

```
        return round(self.calls * self.pace_s)
```

New text:

```
        return round(self.calls * 1.0)
```

### `u191.M9_pace_not_configured`

estimate: the default pace instead of the configured one

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u191.json`, row `M9_pace_not_configured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_the_estimate_reads_the_configured_pace`

Old text:

```
        pace_s=float(cfg.provider.min_interval_s),
```

New text:

```
        pace_s=1.0,
```

### `u193.M24_crawl_over_ceiling_dropped`

Estimate.over: the crawl gate no longer asks when only the ceiling is passed

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u193.json`, row `M24_crawl_over_ceiling_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_a_ceiling_raised_low_for_the_run_is_said_at_the_crawl_gate`
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`

Old text:

```
        return self.calls > FULL_BUILD_CALLS or self.over_ceiling
```

New text:

```
        return self.calls > FULL_BUILD_CALLS
```

### `u193.M25_crawl_spent_ignored`

Estimate.over_ceiling: ignore the calls the listing already spent

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u193.json`, row `M25_crawl_spent_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return self.spent + self.calls > self.ceiling
```

New text:

```
        return self.calls > self.ceiling
```

### `u217.S3_playlists_line`

estimate: carry no listing sentence to the crawl gate

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u217.json`, row `S3_playlists_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_playlists_releases.py`
- Collected: 62 against a baseline of 62
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_the_playlists_crawl_gate_says_the_listing_was_kept`

Old text:

```
        listing=listed.kept.said() if listed.kept is not None else "",
```

New text:

```
        listing="",
```

### `u243.L12_suppressed_releases_unjudged`

playlists_cli.read_catalogue: the tracks of a release the tombstone suppressed are not judged, so a removed single stays on its year

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u243.json`, row `L12_suppressed_releases_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_removed_single_is_taken_off_though_its_release_is_suppressed`
  - `tests/test_label_tombstoned.py::test_hearing_never_merges_back_a_removed_single`

Old text:

```
        tombstoned=tuple(sorted({*grouped.tombstoned, *held_back})),
```

New text:

```
        tombstoned=grouped.tombstoned,
```

### `u243.L5_build_adds_a_tombstoned_track`

playlists_cli._group: a tombstoned track is not left out of its year, so a build adds it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u243.json`, row `L5_build_adds_a_tombstoned_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_build_onto_an_adopted_year_does_not_add_a_removed_track`
  - `tests/test_label_tombstoned.py::test_a_full_build_never_adds_a_tombstoned_track`
  - `tests/test_label_tombstoned.py::test_a_kept_read_judges_a_track_by_the_words_it_kept`
  - `tests/test_label_tombstoned.py::test_a_releases_build_never_adds_a_tombstoned_track`
  - `tests/test_label_tombstoned.py::test_a_releases_build_of_a_wholly_removed_release_says_why`
  - `tests/test_label_tombstoned.py::test_a_year_every_track_of_which_was_removed_is_not_made`

Old text:

```
            if identifier in taken_away:
                emptied_by.add(year)
                continue
```

New text:

```
            if identifier in taken_away:
                emptied_by.add(year)
```

### `u243.L6_empty_years_kept`

playlists_cli._group: a year emptied by removals is still planned, so an empty playlist is made

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u243.json`, row `L6_empty_years_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 140 against a baseline of 140
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_releases_build_of_a_wholly_removed_release_says_why`
  - `tests/test_label_tombstoned.py::test_a_year_every_track_of_which_was_removed_is_not_made`

Old text:

```
            if ids or year not in emptied_by
```

New text:

```
            if True
```

### `r227.C5_favorites_limit_spelled`

sync favorites judges against a seven spelled in the shell

- File: `src/cratekit/favorites/cli.py`
- Source: `r227.json`, row `C5_favorites_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_sync_all.py`
- Collected: 240 against a baseline of 240
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
    for track_id in in_export:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    return replace(

```

New text:

```
    for track_id in library.entries:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    return replace(

```

### `r228-operator.D12_missing_pink_queued`

union_with_pink: queue pink rows the export lacks

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D12_missing_pink_queued`
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
    for track_id in pink_ids:
        if track_id in library.entries:
            in_export.append(track_id)
        else:
            missing.append(track_id)

```

New text:

```
    for track_id in pink_ids:
        in_export.append(track_id)

```

### `r228-operator.D4_union_playlist_first`

union_with_pink: emit pink only rows before playlist members

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D4_union_playlist_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_pink.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_pink.py::test_pink_missing_is_warned_beside_dangling`

Old text:

```
    for track_id in playlist.track_ids:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    for track_id in in_export:
```

New text:

```
    for track_id in in_export:
        if track_id in seen:
            continue
        seen.add(track_id)
        kept.append(track_id)
    for track_id in playlist.track_ids:
```

### `r228-operator.D5_pink_missing_dropped`

union_with_pink: drop pink rows the export lacks instead of naming them

- File: `src/cratekit/favorites/cli.py`
- Source: `r228-operator.json`, row `D5_pink_missing_dropped`
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
        else:
            missing.append(track_id)
```

New text:

```
        else:
            pass
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
- Collected: 240 against a baseline of 240
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
- Collected: 240 against a baseline of 240
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

### `r424.B4_warning_copied`

Hand callers the module level dict instead of a copy per call

- File: `src/cratekit/favorites/cli.py`
- Source: `r424.json`, row `B4_warning_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return (dict(LOCAL_WRITE_WARNING),)
```

New text:

```
    return (LOCAL_WRITE_WARNING,)
```

### `r856-a.F10_concluded_passed`

favorites.sync_favorites: pass no concluded hook to the resume, so a sweep with unmatched favourites carries no warning

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F10_concluded_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 180 against a baseline of 180
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_report_written_before_the_listing_still_names_its_unmatched_rows`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    for item in report.get("unmatched") or ():
```

New text:

```
    for item in [one.get("row") for one in said]:
```

### `r856-a.F6_no_match_sentence`

favorites._left_out: leave the reason empty when the account gave none, so the line reads no reason given

- File: `src/cratekit/favorites/cli.py`
- Source: `r856-a.json`, row `F6_no_match_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 125 against a baseline of 125
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
- Collected: 125 against a baseline of 125
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

### `u117-operator.D10_no_folder_refusal`

apply: drop the missing folder refusal, so a dated playlist is made at the account root

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D10_no_folder_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_label_with_no_folder_yet_refuses_the_apply_before_any_write`

Old text:

```
    if not folder_id:
        raise _no_folder(planned)
```

New text:

```
(empty)
```

### `u117-operator.D11_part_way_named`

apply: a failure part way is raised bare, without what was written

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D11_part_way_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`

Old text:

```
        raise _failed_part_way(exc, done, planned) from exc
```

New text:

```
        raise
```

### `u117-operator.D12_move_into_folder`

apply: a created dated playlist is not moved into the label's folder

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D12_move_into_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_go_into_an_existing_year_makes_a_dated_playlist_and_leaves_the_year`
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
                account.move_to_folder(remote_id, folder_id)
```

New text:

```
                pass
```

### `u117-operator.D15_playable_only`

plan: take every track of a release, playable or not, so an unplayable track is planned on every run

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D15_playable_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`

Old text:

```
        held.extend(one for one in tracks if one in playable and one not in held)
```

New text:

```
        held.extend(one for one in tracks if one not in held)
```

### `u117-operator.D16_recorded_before_move`

apply: record the created playlist only after the move, so a move refused after the create reports nothing written

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D16_recorded_before_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_move_refused_after_the_create_names_the_playlist_left_at_the_root`

Old text:

```
                done.unplaced.append(step.name)
                account.move_to_folder(remote_id, folder_id)
```

New text:

```
                account.move_to_folder(remote_id, folder_id)
                done.unplaced.append(step.name)
```

### `u117-operator.D1_heard_left_out`

plan: drop the heard check, so a release the record lists as heard is filed into the dated playlist again

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D1_heard_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_heard_release_is_left_out_and_the_record_is_not_written`

Old text:

```
        if identity in gone:
```

New text:

```
        if False:
```

### `u117-operator.D2_unsettled_taken`

taken_by_goes: drop the settled check, so an answer no go has taken files its releases as downloaded

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D2_unsettled_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unsettled_or_not_now_answer_took_nothing`

Old text:

```
        if not isinstance(settled, Mapping):
            continue
```

New text:

```
        if not isinstance(settled, Mapping):
            settled = {"at": "2026-10-09T12:00:00+00:00"}
```

### `u117-operator.D4_local_day`

_local_day: keep the recorded UTC day instead of the local one, so a go at 22:00 local west of UTC is filed under tomorrow; killed by the evening instant test

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D4_local_day`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_go_into_an_existing_year_makes_a_dated_playlist_and_leaves_the_year`
  - `tests/test_label_dated.py::test_a_go_on_another_day_makes_its_own_dated_playlist`
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_an_evening_go_west_of_utc_keeps_its_local_day`
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
    if moment.tzinfo is not None:
        moment = moment.astimezone()
```

New text:

```
    if moment.tzinfo is not None:
        moment = moment
```

### `u117-operator.D5_reuse_by_name`

plan: never reuse a dated playlist by its name, so a second go the same day makes a second playlist

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D5_reuse_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
        matching = sorted(pid for pid, title in inside.items() if title == name)
```

New text:

```
        matching = []
```

### `u117-operator.D6_reuse_adds_only_missing`

plan: a reused dated playlist adds every track again rather than only the missing ones

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D6_reuse_adds_only_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_dated.py::test_a_second_go_the_same_day_appends_to_the_same_dated_playlist`
  - `tests/test_label_dated.py::test_a_track_the_provider_will_not_play_is_never_planned_on_the_dated_path`
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_account_refusing_mid_pass_names_what_was_written_and_a_rerun_finishes`

Old text:

```
                    add=tuple(one for one in tracks if one not in have),
```

New text:

```
                    add=tuple(tracks),
```

### `u117-operator.D7_ambiguous`

plan: two playlists with the dated name reuse the first instead of being left alone

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D7_ambiguous`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_two_playlists_with_the_dated_name_are_left_alone`

Old text:

```
        if len(matching) > 1:
```

New text:

```
        if len(matching) > 99:
```

### `u117-operator.D8_age_bound`

_aged: report at the age rather than past it, an off by one on the bound

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D8_age_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_organize_reports_a_dated_playlist_past_the_age_and_moves_nothing`
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
        if days > limit:
```

New text:

```
        if days > limit * 2:
```

### `u117-operator.D9_age_configured`

plan: ignore the configured age and use the default

- File: `src/cratekit/label/dated.py`
- Source: `u117-operator.json`, row `D9_age_configured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_the_age_is_the_configured_one`

Old text:

```
        aged=_aged(catalogue.name, inside, today, cfg.labels.new_playlist_age_days),
```

New text:

```
        aged=_aged(catalogue.name, inside, today, 30),
```

### `u123.D1_dated_create_vouched`

Create a dated playlist without recording it in the ledger

- File: `src/cratekit/label/dated.py`
- Source: `u123.json`, row `D1_dated_create_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`
- Collected: 60 against a baseline of 60
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`
  - `tests/test_label_heard.py::test_declined_nothing_is_written`
  - `tests/test_label_heard.py::test_every_run_says_the_record_labels_tree_is_not_changed`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`
  - `tests/test_label_heard.py::test_some_releases_heard_take_their_tracks_off_and_the_last_removes_it`
  - `tests/test_label_heard.py::test_the_merge_adds_only_what_the_year_lacks_and_never_a_duplicate`
  - `tests/test_label_heard.py::test_what_the_merge_adds_to_a_recorded_year_is_recorded_on_it`

Old text:

```
                remote_id = ledger.reserve_label_dated(
                    cfg,
                    planned.label_id,
                    step.name,
                    lambda name=step.name: account.create_playlist(name),
                )
```

New text:

```
                remote_id = account.create_playlist(step.name)
```

### `u191.M21_unsettled_answers_read`

taken_by_goes: read an answer no go has settled (existing guard, newly on this unit's path)

- File: `src/cratekit/label/dated.py`
- Source: `u191.json`, row `M21_unsettled_answers_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_releases.py`, `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unsettled_or_not_now_answer_took_nothing`
  - `tests/test_label_playlists_releases.py::test_an_answer_no_go_has_taken_is_not_read`

Old text:

```
        if not isinstance(settled, Mapping):
            continue
```

New text:

```
        if not isinstance(settled, Mapping):
            settled = {"at": "2026-10-31T12:00:00+00:00"}
```

### `u100-a.H1a_rejected_adopted`

harvest.decided reads any settled verdict as accepted, so a rejected label is adopted

- File: `src/cratekit/label/harvest.py`
- Source: `u100-a.json`, row `H1a_rejected_adopted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`
- Collected: 335 against a baseline of 335
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_rejected_or_open_label_is_not_added`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
        if item.verdict is review.Verdict.ACCEPTED:
```

New text:

```
        if item.verdict is not None:
```

### `u100-a.H1b_open_adopted`

harvest.decided reads anything not rejected as accepted, so an open label is adopted

- File: `src/cratekit/label/harvest.py`
- Source: `u100-a.json`, row `H1b_open_adopted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`
- Collected: 335 against a baseline of 335
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_rejected_or_open_label_is_not_added`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`

Old text:

```
        if item.verdict is review.Verdict.ACCEPTED:
```

New text:

```
        if item.verdict is not review.Verdict.REJECTED:
```

### `u100-a.H2_kind_filter`

harvest.decided drops the harvested-label kind filter, so an accepted sweep release on the same queue is adopted as a label

- File: `src/cratekit/label/harvest.py`
- Source: `u100-a.json`, row `H2_kind_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`
- Collected: 335 against a baseline of 335
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_label_release_on_the_same_queue_is_not_adopted`

Old text:

```
        kinds=(KIND,),
```

New text:

```
        kinds=None,
```

### `u100-a.H3_resolved_excluded`

harvest.decided lists open items only, so no accepted verdict is ever read

- File: `src/cratekit/label/harvest.py`
- Source: `u100-a.json`, row `H3_resolved_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`
- Collected: 335 against a baseline of 335
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`
  - `tests/test_label_registry_adopt.py::test_a_person_reading_the_default_output_sees_what_was_added`
  - `tests/test_label_registry_adopt.py::test_a_rejected_or_open_label_is_not_added`
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_nothing_accepted_writes_nothing_and_says_what_is_waiting`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
        include_resolved=True,
```

New text:

```
        include_resolved=False,
```

### `u100-a.H4_nameless_dropped`

an accepted item naming no label is skipped silently instead of reported

- File: `src/cratekit/label/harvest.py`
- Source: `u100-a.json`, row `H4_nameless_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`
- Collected: 335 against a baseline of 335
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_accepted_item_naming_no_label_is_reported_not_skipped`

Old text:

```
                nameless.append(item.item_id)
```

New text:

```
                pass
```

### `u237.M1_bare_letter_is_a_mark_again`

_YEAR: make the parentheses optional again, so a bare leading P or C is stripped as a mark (Cadenza reads adenza)

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M1_bare_letter_is_a_mark_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 33 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(C) ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(P)]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(C) ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(P)]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(C) ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(P)]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\(?[PC]\)?|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

### `u237.M2_symbol_marks_dropped`

_YEAR: forget the sound recording and copyright symbols, so a line starting with one keeps its mark and year

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M2_symbol_marks_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 36 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\xa9 ]`
  - ... and 21 more, see the JSON sidecar

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\))\s*)+", re.IGNORECASE)
```

### `u237.M3_one_mark_only`

_YEAR: strip one mark only, so (P)(C) 2021 Cadenza keeps the second mark and the year

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M3_one_mark_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 12 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-\u2117 \xa9 2021 ]`

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)", re.IGNORECASE)
```

### `u237.M4_case_sensitive_mark`

_YEAR: drop the case fold, so a lower case (p) mark is kept as part of the name

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M4_case_sensitive_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 12 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-(p) 2021 ]`

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+")
```

### `u237.M5_bare_year_is_a_label`

_YEAR_NUM: strip a year only when a name follows, so a line of a mark and a year offers the year as a label

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M5_bare_year_is_a_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[(P) 2021-expected10]`
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[(P) 2021.-expected11]`
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[2021-expected14]`
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[\u2117 2021-expected13]`

Old text:

```
_YEAR_NUM = re.compile(r"^\d{4}(?:\s+|\.?$)")
```

New text:

```
_YEAR_NUM = re.compile(r"^\d{4}\s+")
```

### `u237.M9_year_eats_the_next_digit`

_YEAR_NUM: drop the boundary after the year, so 20211 Label reads 1 Label

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M9_year_eats_the_next_digit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[20211 Label-expected12]`

Old text:

```
_YEAR_NUM = re.compile(r"^\d{4}(?:\s+|\.?$)")
```

New text:

```
_YEAR_NUM = re.compile(r"^\d{4}\s*")
```

### `u252.L7_seam_drops_keywords`

harvest.playlist_tracks: stop handing its keywords to the listing, so the fixture's sleep never reaches the ladder

- File: `src/cratekit/label/harvest.py`
- Source: `u252.json`, row `L7_seam_drops_keywords`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
    return listing.playlist_tracks(playlist, **kwargs)
```

New text:

```
    return listing.playlist_tracks(playlist)
```

### `r382.M16_parser_moved_lowercase`

The moved parser keeps a bare identifier's case, checking the move kept its tests

- File: `src/cratekit/label/catalogue.py`
- Source: `r382.json`, row `M16_parser_moved_lowercase`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 891 against a baseline of 891
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_url_a_share_link_and_a_bare_id_all_name_the_playlist[bare-upper]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`

Old text:

```
    if _UUID.fullmatch(text):
        return text.lower()
```

New text:

```
    if _UUID.fullmatch(text):
        return text
```

### `r515-operator.S1_of_takes_bool`

Let ListingShortfall.of trust a bool as a declared count

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S1_of_takes_bool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[True]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if not isinstance(declared, int) or declared <= 0:
```

### `r515-operator.S2_of_takes_non_int`

Let ListingShortfall.of trust a count that is not an integer

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S2_of_takes_non_int`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_that_is_not_a_usable_count_leaves_nothing_to_compare[10]`

Old text:

```
        if isinstance(declared, bool) or not isinstance(declared, int) or declared <= 0:
```

New text:

```
        if isinstance(declared, bool) or declared is None or declared <= 0:
```

### `r515-operator.S4_of_short_at_count`

Mint a shortfall when the listing reaches the count exactly

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S4_of_short_at_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_full_release_carries_no_shortfall`

Old text:

```
        if listed >= declared:
```

New text:

```
        if listed > declared:
```

### `r515-operator.S5_of_short_over_count`

Mint a shortfall when the listing runs past the count

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S5_of_short_over_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_that_serves_more_than_its_declared_count_carries_no_shortfall`

Old text:

```
        if listed >= declared:
```

New text:

```
        if listed == declared:
```

### `r515-operator.S6_cache_drops_short`

The caching release reader stores the rows and year but drops the shortfall

- File: `src/cratekit/label/catalogue.py`
- Source: `r515-operator.json`, row `S6_cache_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
        answer = (tuple(rows), year, short)
```

New text:

```
        answer = (tuple(rows), year, None)
```

### `r815-a.G2_forgetting_keeps_the_failure_count`

ReleaseTracks.forget: forget the failures in a row as well

- File: `src/cratekit/label/catalogue.py`
- Source: `r815-a.json`, row `G2_forgetting_keeps_the_failure_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`
- Collected: 214 against a baseline of 214
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_reader_forgets_each_release_and_keeps_its_count_of_failures`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
        self._read.clear()

    def release_tracks
```

New text:

```
        self._read.clear()
        self._failed_in_a_row = 0

    def release_tracks
```

### `r840-c.C4_no_name_is_the_empty_string`

artist_name: answer with the text of whatever the artist's name attribute holds, so an object with no name reads None

- File: `src/cratekit/label/catalogue.py`
- Source: `r840-c.json`, row `C4_no_name_is_the_empty_string`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`
- Collected: 354 against a baseline of 354
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`

Old text:

```
    return name if isinstance(name, str) else ""
```

New text:

```
    return str(name)
```

### `u62.C2_outage_as_credential`

Refuse an unreachable provider as a credential problem

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C2_outage_as_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 544 against a baseline of 544
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
    except ProviderUnavailable as exc:
        raise refuse(
            "unavailable-transient",
```

New text:

```
    except ProviderUnavailable as exc:
        raise refuse(
            "credential-missing",
```

### `u97-b.B3_label_path_raises_the_other_token`

catalogue.resolve: refuse a missing session with REAUTHENTICATE_PROVIDER, so a person who never had one is told theirs was rejected

- File: `src/cratekit/label/catalogue.py`
- Source: `u97-b.json`, row `B3_label_path_raises_the_other_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
            remedy=Remedy.AUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
```

New text:

```
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
            scope=Scope.RUN,
            origin=("label", "catalogue"),
```

### `u237.M10_empty_sides_match`

labels_match: drop the guard on empty folds, so two names that both fold to nothing confirm each other

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M10_empty_sides_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[***----]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[\u65e5\u672c-\u041f\u043b\u0430\u0441\u0442\u0438\u043d\u043a\u0430]`

Old text:

```
    return bool(left) and bool(right) and (_words_within(left, right) or _words_within(right, left))
```

New text:

```
    return _words_within(left, right) or _words_within(right, left)
```

### `u237.M6_substring_again`

_words_within: back to a raw substring, so the Rawax needle confirms RAWAXXX

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M6_substring_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Puls-Pulse]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[RAWAXXX-Rawax]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-RAWAXXX]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-Rawaxxx Records]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[adenza-Cadenza]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[ronos-Cronos]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[tide-Tidewater]`
  - `tests/modules/test_labels.py::test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
    return f" {needle} " in f" {credit} "
```

New text:

```
    return needle in credit
```

### `u237.M7_left_word_boundary_only`

_words_within: pad only the front, so a needle that is a word's prefix still confirms

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M7_left_word_boundary_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Puls-Pulse]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[RAWAXXX-Rawax]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-RAWAXXX]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-Rawaxxx Records]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[tide-Tidewater]`
  - `tests/modules/test_labels.py::test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
    return f" {needle} " in f" {credit} "
```

New text:

```
    return f" {needle}" in f" {credit} "
```

### `u237.M8_one_direction_only`

labels_match: drop the credit inside the needle direction, so a needle Rawax Records no longer confirms a credit Rawax

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M8_one_direction_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_confirms_its_label_on_whole_words[Rawax Records-Rawax]`

Old text:

```
(_words_within(left, right) or _words_within(right, left))
```

New text:

```
_words_within(left, right)
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

### `u145.V1_gate_on_nothing`

favorites_split: a library with no quarter is still put to the gate

- File: `src/cratekit/favorites/split_cli.py`
- Source: `u145.json`, row `V1_gate_on_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_a_library_with_no_quarter_never_walks_the_library_or_asks_the_account`
  - `tests/test_favorites_split.py::test_a_second_run_plans_nothing_and_opens_no_gate`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u145.V2_no_ack`

favorites_split: the backup acknowledgment is not read before the plan

- File: `src/cratekit/favorites/split_cli.py`
- Source: `u145.json`, row `V2_no_ack`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_split.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u120.V1_no_ack`

favorites_backfill: the acknowledgment is not read before the gate

- File: `src/cratekit/favorites/backfill_cli.py`
- Source: `u120.json`, row `V1_no_ack`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = planned(cfg, source=source)
```

New text:

```
    plan = planned(cfg, source=source)
```

### `r836-g.C1_holds_judged_again`

label.prune_cli.held_releases: a hold the gate would now release still takes the release's tracks off

- File: `src/cratekit/label/prune_cli.py`
- Source: `r836-g.json`, row `C1_holds_judged_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_hold_the_gate_would_now_release_takes_nothing_off`

Old text:

```
        and (hold.payload.get(review.WITHHELD_FIELD) or judge.rejudge(entry, hold).held)
```

New text:

```
(empty)
```

