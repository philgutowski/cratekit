# Mutation table: u334-replay-before-6

Measured by `scripts/mutate.py` on 2026-11-24 04:09 UTC, branch `HEAD` at `89c9e120`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 310.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:09 UTC for commit `89c9e120f5d4`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 42, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u108-d.G11_waited_go_refuses_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-d.G14_retryable_cause_only_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 1 | killed |
| `u108-d.G16_origin_marker_filter_again` | `src/cratekit/label/go.py` | user | 1 file(s) | 110 | 7 | killed |
| `u110-c.C4_go_tail` | `src/cratekit/label/go.py` | user | 2 file(s) | 130 | 2 | killed |
| `u190.G5_resume_one_job_only` | `src/cratekit/label/go.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u239-composites.M11b_land_only_landed_after_its_test` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 3 | killed |
| `u239.M01_own_needs_apply` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M02_own_skips_cancelled` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M03_own_job_by_run` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 13 | killed |
| `u239.M04_go_takes_own_on` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 19 | killed |
| `u239.M05_beside_later_only` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 8 | killed |
| `u239.M06_beside_open` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M07_beside_done` | `src/cratekit/label/go.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u239.M08_retry_half_failed` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M09_named_landing` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 4 | killed |
| `u239.M14_ceiling_fresh` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u239.M15_ceiling_job_id` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.M16_other_stop_step` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.M17_wrote` | `src/cratekit/label/go.py` | user | 3 file(s) | 276 | 1 | killed |
| `u100-a.H1a_rejected_adopted` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 2 | killed |
| `u100-a.H1b_open_adopted` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 2 | killed |
| `u100-a.H2_kind_filter` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 1 | killed |
| `u100-a.H3_resolved_excluded` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 11 | killed |
| `u100-a.H4_nameless_dropped` | `src/cratekit/label/harvest.py` | user | 4 file(s) | 335 | 1 | killed |
| `u237.M2_symbol_marks_dropped` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 36 | killed |
| `u243.L11_heard_adds_a_tombstoned_track` | `src/cratekit/label/heard.py` | user | 2 file(s) | 68 | 3 | killed |
| `u243.L13_heard_merges_a_pruned_track` | `src/cratekit/label/heard.py` | user | 2 file(s) | 68 | 1 | killed |
| `r1091.K10_available_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K11_year_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K12_periodic_write_off` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K13_write_error_raised` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 6 | killed |
| `r1091.K14_unkept_never_cleared` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K15_reuse_uncounted` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 3 | killed |
| `r1091.K1_age_never_expires` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K2_future_is_fresh` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K3_age_boundary` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K4_age_coefficient` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 4 | killed |
| `r1091.K5_version_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K6_label_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K7_gone_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K8_year_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K9_track_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `u243.L7_kept_read_judged_blind` | `src/cratekit/label/kept_reads.py` | user | 2 file(s) | 74 | 4 | killed |
| `u308.L9_store_flushes_nothing` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 138 | 42 | killed |
| `r381-b.M14_follow_all_renames` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M13_follow_overwrites` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M15_read_does_not_persist` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M16_advance_does_not_follow` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
| `r381.M17_read_no_follow` | `src/cratekit/label/marks.py` | user | 2 file(s) | 208 | 1 | killed |
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
| `u191.M10_crawl_digest_count` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u191.M11_releases_scope_unmarked` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 1 | killed |
| `u191.M12_empty_releases_plan_makes_folder` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 4 | killed |
| `u191.M13_gone_refused` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 42 | killed |
| `u191.M14_review_item_identity_asked` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u191.M15_nothing_left_said_as_nothing_taken` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M16_recorded_year_unchecked` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 1 | killed |
| `u191.M18_listing_relisted` | `src/cratekit/label/playlists_cli.py` | maintainer | 2 file(s) | 80 | 1 | killed |
| `u191.M1_crawl_gate_skipped` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 5 | killed |
| `u191.M2_crawl_declined_crawls` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 1 | killed |
| `u191.M3_crawl_asks_the_build_gate` | `src/cratekit/label/playlists_cli.py` | user | 2 file(s) | 80 | 5 | killed |
| `u191.M4_threshold_boundary` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M5_threshold_value` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M6_calls_per_release_coefficient` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 5 | killed |
| `u191.M8_time_ignores_pace` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u191.M9_pace_not_configured` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u193.M24_crawl_over_ceiling_dropped` | `src/cratekit/label/playlists_cli.py` | user | 5 file(s) | 523 | 2 | killed |
| `u193.M25_crawl_spent_ignored` | `src/cratekit/label/playlists_cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u243.L12_suppressed_releases_unjudged` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 134 | 2 | killed |
| `u243.L5_build_adds_a_tombstoned_track` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 134 | 6 | killed |
| `u243.L6_empty_years_kept` | `src/cratekit/label/playlists_cli.py` | user | 3 file(s) | 134 | 2 | killed |
| `r836-g.C1_holds_judged_again` | `src/cratekit/label/prune_cli.py` | user | 5 file(s) | 404 | 1 | killed |
| `r381-b.M12_add_legacy_any_name` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M10_by_id_no_follow` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M11_add_ignores_legacy` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M1_fold_only_slug` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 13 | killed |
| `r381.M2_no_umlaut_table` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 6 | killed |
| `r381.M3_keep_combining_marks` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 10 | killed |
| `r381.M4_migrate_ignores_taken` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r381.M5_migrate_any_identifier` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r381.M6_update_skips_move_write` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 1 | killed |
| `r381.M7_load_never_migrates` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r381.M8_no_renamed_map` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `r381.M9_live_renames_unfiltered` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 2 | killed |
| `u100-a.R1_slug_only_presence` | `src/cratekit/label/registry.py` | user | 4 file(s) | 23216 | 0 (promoted) | zero |
| `u100-a.R2_no_presence_check` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 6 | killed |
| `u100-a.R3_presence_before_the_batch` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u100-a.R4_slug_refusal_aborts` | `src/cratekit/label/registry.py` | user | 4 file(s) | 401 | 1 | killed |
| `u100-c.R5_adopt_always_writes_after_fix` | `src/cratekit/label/registry.py` | user | 1 file(s) | 16 | 1 | killed |
| `u341.G1_of_genre_any_genre` | `src/cratekit/label/registry.py` | user | 5 file(s) | 410 | 13 | killed |
| `u341.G2_of_genre_unfolded` | `src/cratekit/label/registry.py` | user | 5 file(s) | 410 | 3 | killed |
| `u341.G3_genres_not_folded_once` | `src/cratekit/label/registry.py` | user | 5 file(s) | 410 | 1 | killed |
| `u99-a.A10_edit_drops_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A11_edit_drops_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A12_edit_drops_limit` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A13_by_name_unnormalized` | `src/cratekit/label/registry.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u99-a.A1_blank_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A2_malformed_id_seed` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A3_id_prefix_case` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A4_id_digits_optional` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-a.A5_id_prefix_match` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 2 | killed |
| `u99-a.A7_add_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 7 | killed |
| `u99-a.A8_edit_unchecked_seeds` | `src/cratekit/label/registry.py` | user | 3 file(s) | 293 | 1 | killed |
| `u99-b.A6r_store_limit_floor` | `src/cratekit/label/registry.py` | maintainer | 3 file(s) | 293 | 1 | killed |
| `u308.L5_extended_step_dropped` | `src/cratekit/label/review_common.py` | user | 3 file(s) | 247 | 8 | killed |
| `u308.L6_ended_outcome_ignored` | `src/cratekit/label/review_common.py` | user | 4 file(s) | 366 | 20 | killed |
| `r259-b.O2_unreadable_row` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r259.L2_library_kwarg` | `src/cratekit/label/sweep.py` | maintainer | 5 file(s) | 524 | 1 | killed |
| `r259.O1_no_tracks_guard` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r259.O5_memo` | `src/cratekit/label/sweep.py` | maintainer | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r261.S1_roster_unread_read` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 2 | killed |
| `r261.S2_own_missing` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.S3_source_collects` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 522 | 3 | killed |
| `r704-a.S1_no_cause_chain_check` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 6 | killed |
| `r704-a.S7_probe_unclassified` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `r704-a.S8_crawl_unclassified` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 2 | killed |
| `r704-a.S9_resolve_unclassified` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `u107-a.S06_queued_also` | `src/cratekit/label/sweep.py` | user | 10 file(s) | 933 | 8 | killed |
| `u238.M4_beyond_leaves_out_unchecked` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 472 | 19 | killed |
| `u238.M5_window_edge_off_by_one` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 472 | 13 | killed |
| `u277.M3_another_label_before_no_line` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 309 | 12 | killed |
| `u277.M8_past_window_counts_other_labels` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 309 | 6 | killed |
| `u52-item-derivation.S5_dropped_never_accumulated` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 3 | killed |
| `u52-zero-rows.P1_revoked_tombstones_suppress` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `u52-zero-rows.P2_snapshot_read_eagerly` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `r1114.M10_message_reworded_many` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M11_message_reworded_one` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M12_match_step_dropped` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M13_detail_labels_empty` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M14_withheld_reads_no_op` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M15_skipped_line_not_fail` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 5 | killed |
| `r1114.M16_remedy_line_dropped` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 2 | killed |
| `r1114.M17_remedy_line_only_doctor` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M1_every_skipped_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 3 | killed |
| `r1114.M2_single_label_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M3_mixed_run_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M4_closing_line_ignores_skips` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M5_closing_line_names_every_label` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r1114.M6_nothing_new_not_counted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 13 | killed |
| `r1114.M7_refusal_drops_the_lines` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 3 | killed |
| `r1114.M8_refusal_not_retryable` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `r515-operator.S8_short_of_keeps_zero` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `r515-operator.S9_question_no_short` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-a.S03_marker_moves` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 13 | killed |
| `u107-a.S04_marker_takes_window_place` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 8 | killed |
| `u107-a.S07_gate_before_asking` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-a.S08_catch_up_withhold` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 2 | killed |
| `u107-b.S10_pick_unknown` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 2 | killed |
| `u107-b.S11_pick_takes_only_chosen` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 7 | killed |
| `u107-b.S12_stop_removes` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 3 | killed |
| `u107-b.S13_take_accepts` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 10 | killed |
| `u107-b.S15_no_default_answer` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-b.S16_save_before_ask` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 9 | killed |
| `u107-b.S17_dead_verifier_skip` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-c.S20_pick_isdecimal` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-c.S21_filing_run` | `src/cratekit/label/sync_cli.py` | maintainer | 1 file(s) | 95 | 1 | killed |
| `u107-c.S23_stop_remedy` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-c.S24_size_coefficient` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 2 | killed |
| `u107-d.S02_record_version_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-d.S14_take_respects_decided_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u107-d.S25_measured_passes_refusal_again` | `src/cratekit/label/sync_cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u108-a.G01_unsettled_skips_settled` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 4 | killed |
| `u108-c.G19_settle_keeps` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u108-c.G24_walk_ends_at_gate` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 8 | killed |
| `u108-d.G18_settle_matches_identity_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u108-d.G20_settle_skips_settled_again` | `src/cratekit/label/sync_cli.py` | maintainer | 2 file(s) | 205 | 1 | killed |
| `u189.M11_answer_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u189.M12_pick_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u189.M13_walk_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u189.M14_pick_no_release_remedy_plain_next` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 3 | killed |
| `u189.M15_pick_remedy_unquoted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 3 | killed |
| `u189.M16_empty_label_alone_walks` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u189.M1_next_label_refused_again` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 12 | killed |
| `u189.M2_label_alone_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 5 | killed |
| `u189.M3_next_release_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 2 | killed |
| `u189.M4_empty_name_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 2 | killed |
| `u189.M5_alone_hint_drops_the_label` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 3 | killed |
| `u189.M7_unknown_name_not_refused` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 2 | killed |
| `u189.S1_saved_question_relisted` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 4 | killed |
| `u189.S2_question_not_saved` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 119 | killed |
| `u238.M10_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 321 | 3 | killed |
| `u238.M11_saved_question_drops_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 321 | 3 | killed |
| `u238.M7_old_question_read_as_count` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 321 | 5 | killed |
| `u238.M8_bound_said_as_the_labels` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 321 | 8 | killed |
| `u238.M9_nothing_line_loses_the_split` | `src/cratekit/label/sync_cli.py` | user | 3 file(s) | 321 | 2 | killed |
| `u278.M24_label_sync_not_narrowed` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 385 | 3 | killed |
| `u278.M25_sweep_never_refuses` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 385 | 3 | killed |
| `u308.L1_record_lock_refusal_lost` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 205 | 1 | killed |
| `u341.G10_asked_every_label` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 7 | killed |
| `u341.G11_walk_drops_genre` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 13 | killed |
| `u341.G12_next_drops_genre` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 5 | killed |
| `u341.G13_selection_guard_dropped` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 5 | killed |
| `u341.G14_selection_guard_without_label` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 2 | killed |
| `u341.G15_resume_hint_unnamed` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 2 | killed |
| `u341.G16_gate_shows_group_line` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 1 | killed |
| `u341.G17_answer_hint_leaves_group` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 4 | killed |
| `u341.G18_unanswerable_hint_leaves_group` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 1 | killed |
| `u341.G19_budget_wording_unnamed` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 377 | 2 | killed |
| `u341.G20_hint_into_a_dissolved_group` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 1 | killed |
| `u341.G21_hint_quoted_as_repr` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 425 | 1 | killed |
| `r1313.C1_catalogue_failure_alone` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 5 | killed |
| `r1313.C2_catalogue_name_on_any_link` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 1 | killed |
| `r261.D1_discovery_record` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `r261.D2_transient_class` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.D3_held_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.R2_roster_keeps_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `r351.A2_unresolved_seed_skipped` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r351.A3_empty_roster_returned` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 6 | killed |
| `r351.A5_ambiguity_takes_first` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r351.G10_identifier_message_says_named` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G3_unresolved_id_skipped` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 5 | killed |
| `r351.G4_any_remainder_is_an_id` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G5_except_everything` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r351.G7_drop_object_not_found` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G8_id_prefix_case_insensitive` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r351.G9_all_lookuperror_is_absence` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.A2_empty_roster_returned` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 6 | killed |
| `r352.G10_no_collaborator_enqueue` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G11_discovered_not_added` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 10 | killed |
| `r352.G13_duplicate_roster_member` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G2_skip_when_roster_nonempty` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 7 | killed |
| `r352.G4_empty_message_omits_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r352.G5_compilation_range_shrunk` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r352.G6_name_query_only` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r352.G7_ignore_match_needle` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r504-a.A1_lt_to_le` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `r504-a.A2_lt_to_gt` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 4 | killed |
| `r504-a.A3_no_none_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r504-a.A4_no_raise` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `r515-operator.S7_adapter_no_count` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r705-b.S9_playlist_read_wraps_the_park` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 118 | 1 | killed |
| `r840-c.C3_the_adapter_reads_a_name` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 5 | killed |
| `r879-b.T2_offset_not_sent` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `r888.R1_roster_serves_one_listing` | `src/cratekit/label/tidal_catalogue.py` | user | 5 file(s) | 578 | 3 | killed |
| `u217.A2_roster_lists_now` | `src/cratekit/label/tidal_catalogue.py` | user | 2 file(s) | 212 | 7 | killed |
| `u261.O1_catalogue_drops_the_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 270 | 3 | killed |
| `u62.A1_missing_playlist_returns_none` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A4_first_hit_not_exact` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A6_no_reread_for_missing_copyright` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u62.A7_any_search_hit_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `u70.A1_no_favourites_refused` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 1 | killed |
| `u75-c.C1_gone_is_never_retried` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 4 | killed |
| `u75-c.C5_none_album_raises` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 2 | killed |
| `u75-c.C7_tracks_through_the_paging_wrapper` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 3 | killed |
| `u78-c.D2_blank_isrc` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 3 | killed |
| `u78-c.D3_no_lookup_method` | `src/cratekit/label/tidal_catalogue.py` | maintainer | 1 file(s) | 174 | 1 | killed |
| `u79-c.D1_search_shape_read_as_empty` | `src/cratekit/label/tidal_catalogue.py` | user | 1 file(s) | 174 | 1 | killed |
| `u243.L1_companion_not_asked` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 134 | 1 | killed |
| `u243.L2_revoked_tombstones_count` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 134 | 1 | killed |
| `u243.L3_artists_joined_with_ampersand` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 134 | 2 | killed |
| `u243.L4_title_without_version` | `src/cratekit/label/tombstoned.py` | user | 3 file(s) | 134 | 4 | killed |

## Zero rows and what they owe

- `u190.G5_resume_one_job_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u239.M07_beside_done` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u193.M25_crawl_spent_ignored` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u100-a.R1_slug_only_presence` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u99-a.A13_by_name_unnormalized` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r259.O1_no_tracks_guard` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r259.O5_memo` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u108-d.G11_waited_go_refuses_again`

go.go: a go that waited for the record's lock while another queued goes on to list and queue

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G11_waited_go_refuses_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`

Old text:

```
        if held.resume:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u108-d.G14_retryable_cause_only_again`

go.resumable: a job whose cause says no retry can succeed is resumed anyway

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G14_retryable_cause_only_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_job_whose_failures_cannot_succeed_on_a_retry_is_not_resumed`

Old text:

```
    return job.cause is None or job.cause.retryable
```

New text:

```
    return True
```

### `u108-d.G16_origin_marker_filter_again`

go.held_by_goes: every acquire download job counts as a go's, so a download queued by hand is resumed and its tracks held by the go

- File: `src/cratekit/label/go.py`
- Source: `u108-d.json`, row `G16_origin_marker_filter_again`
- Moved: held_by_goes now asks _goes_job whether a job is a go's; the origin marker test moved there unchanged
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`
- Collected: 110 against a baseline of 110
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_label_sync_go.py::test_a_plain_download_a_tail_renamed_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`

Old text:

```
    return job.handler_key == DOWNLOAD and isinstance((job.payload or {}).get(ORIGIN_KEY), Mapping)
```

New text:

```
    return job.handler_key == DOWNLOAD
```

### `u110-c.C4_go_tail`

The label go tail prints --name RUN again

- File: `src/cratekit/label/go.py`
- Source: `u110-c.json`, row `C4_go_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`, `tests/test_label_sync_go.py`
- Collected: 130 against a baseline of 130
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_the_label_go_tail_hands_the_run_as_the_pass_and_names_no_batch`
  - `tests/test_label_sync_go.py::test_the_download_lands_as_an_intake_under_the_runs_one_batch`

Old text:

```
"--pass", default_name(run_id)]
```

New text:

```
"--name", default_name(run_id)]
```

### `u190.G5_resume_one_job_only`

_resume: take the first earlier job's tail whatever the count, so two manifests share one landing

- File: `src/cratekit/label/go.py`
- Source: `u190.json`, row `G5_resume_one_job_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    land = lands[0] if len(lands) == 1 else None
```

New text:

```
    land = lands[0] if lands else None
```

### `u239-composites.M11b_land_only_landed_after_its_test`

M11 measured again after its test: name the landing whatever the download read

- File: `src/cratekit/label/go.py`
- Source: `u239-composites.json`, row `M11b_land_only_landed_after_its_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
    if read.landed and manifest is not None:
```

New text:

```
    if manifest is not None:
```

### `u239.M01_own_needs_apply`

_own: take the run's job on whatever answer is recorded, so an abort recorded after the stop downloads and lands

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M01_own_needs_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_abort_recorded_after_the_stop_is_not_taken_on`

Old text:

```
    if recorded is None or recorded.option != APPLY:
```

New text:

```
    if recorded is None:
```

### `u239.M02_own_skips_cancelled`

_own: take a cancelled job on too, so a person's cancel is resumed and landed with no question

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M02_own_skips_cancelled`
- Moved: _own returns through one conditional; the cancelled test is the same clause of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`

Old text:

```
    return None if job is None or job.state is jobs.JobState.CANCELLED else job.job_id
```

New text:

```
    return None if job is None else job.job_id
```

### `u239.M03_own_job_by_run`

own_job: take any go job on, not only the one this run's go queued

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M03_own_job_by_run`
- Moved: own_job asks _goes_job for the origin marker; the run match is the same comparison after it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_job_stopped_halfway_resumes_and_downloads_only_the_rest`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_resumed_download_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_second_go_that_waited_for_the_first_refuses_rather_than_queue_its_tracks_again`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[bridge]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if _goes_job(job) and job.payload[ORIGIN_KEY].get("run") == run_id:
```

New text:

```
        if _goes_job(job) and True:
```

### `u239.M04_go_takes_own_on`

go: never take the run's own download on, so the go asks the gate again as before U239

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M04_go_takes_own_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    if own is not None:
```

New text:

```
    if False:
```

### `u239.M05_beside_later_only`

_beside: count earlier go jobs too, so a later run's tail is refused over an earlier landed go

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M05_beside_later_only`
- Moved: _beside folds its two skips into one test; the earlier job clause is the same comparison
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_with_an_earlier_download_to_resume_resumes_it_and_queues_nothing_new`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[bridge]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_download_once_landed_lets_the_fresh_go_ask_and_download[native]`
  - `tests/test_label_sync_go.py::test_an_earlier_gos_landed_download_does_not_refuse_a_later_runs_tail`
  - `tests/test_label_sync_go.py::test_answers_saved_beside_a_finished_go_wait_and_are_not_landed_with_it`

Old text:

```
        if other.job_id == job.job_id or other.created < job.created or not _goes_job(other):
```

New text:

```
        if other.job_id == job.job_id or not _goes_job(other):
```

### `u239.M06_beside_open`

_beside: count only a later go job that downloaded, so one parked before any track is ignored

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M06_beside_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_later_go_parked_before_it_downloaded_anything_still_refuses_the_tail`

Old text:

```
        if other.is_open() or any(
```

New text:

```
        if any(
```

### `u239.M07_beside_done`

_beside: count only an open later go job, so one that downloaded and settled is ignored

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M07_beside_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if other.is_open() or any(
```

New text:

```
        if other.is_open() or False and any(
```

### `u239.M08_retry_half_failed`

_carry_on: never re-arm a half failed own job, so a transient failure ends every go under the run

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M08_retry_half_failed`
- Moved: _carry_on reads the job's items once, so the left count is passed inline to the same resumable test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`

Old text:

```
        if not job.is_open() and resumable(job, _left(items)):
```

New text:

```
        if False:
```

### `u239.M09_named_landing`

_carry_on: ignore the recorded landing, so the tail runs a second time

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M09_named_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        if named:
```

New text:

```
        if False:
```

### `u239.M14_ceiling_fresh`

_carried: drop fresh, so the continue keeps the command line's own --run

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M14_ceiling_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`

Old text:

```
        detail.update({"job": job.job_id, "run_id": run, "fresh": True})
```

New text:

```
        detail.update({"job": job.job_id, "run_id": run})
```

### `u239.M15_ceiling_job_id`

_carried: keep job_id on the ceiling cause, so the continue is job resume again

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M15_ceiling_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`

Old text:

```
        detail = {key: value for key, value in (cause.detail or {}).items() if key != "job_id"}
```

New text:

```
        detail = dict(cause.detail or {})
```

### `u239.M16_other_stop_step`

_carried: add no step to a park or a retryable failure, so it names no way to the landing

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M16_other_stop_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`

Old text:

```
    if job.state is jobs.JobState.BLOCKED or (
```

New text:

```
    if False and (
```

### `u239.M17_wrote`

_carry_on: a walk that wrote answers under a landed run reports no_op

- File: `src/cratekit/label/go.py`
- Source: `u239.json`, row `M17_wrote`
- Moved: the named landing branch of _carry_on returns through the shared _ended helper with the same wrote outcome
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
            return _ended(ctx, checks, report, Outcome.OK if wrote else Outcome.NO_OP)
        items
```

New text:

```
            return _ended(ctx, checks, report, Outcome.NO_OP)
        items
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
- Moved: The same pruned tracks of the recorded year joined to what the year must not hold; the year's ledger record was read twice under two names, so it is now read once as recorded and this line names it so.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_label_heard.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_hearing_never_undoes_a_prune_of_a_held_release`

Old text:

```
        set(recorded.pruned) if recorded is not None else set()
```

New text:

```
        set()
```

### `r1091.K10_available_dropped`

_row: keep every track as playable, so a track the provider will not play is asked for from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K10_available_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year`

Old text:

```
        "available": getattr(track, "available", True) is not False,
```

New text:

```
        "available": True,
```

### `r1091.K11_year_dropped`

keep: store no year, so a release the provider dates is planned under its listed year from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K11_year_dropped`
- Moved: The same stated year kept on a release read; the Kept is now built on one line with its tracks named first, so the year keyword sits inside the _hold call rather than on a line of its own.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one`

Old text:

```
        self._hold(release_id, Kept(read_at=clock(), gone=False, tracks=tracks, year=stated))
```

New text:

```
        self._hold(release_id, Kept(read_at=clock(), gone=False, tracks=tracks, year=None))
```

### `r1091.K12_periodic_write_off`

_hold: never write mid run, so a killed build keeps nothing it read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K12_periodic_write_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_reads_are_written_every_flush_and_not_only_at_the_end`

Old text:

```
        if self._since >= FLUSH_EVERY:
```

New text:

```
        if False:
```

### `r1091.K13_write_error_raised`

flush: let a write the filesystem refuses raise, the round 1 blocking finding

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K13_write_error_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`
  - `tests/test_label_playlists_kept.py::test_an_abort_after_a_failed_write_still_warns_the_reads_were_not_kept`

Old text:

```
        except OSError as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
```

New text:

```
        except OSError as exc:
            raise
```

### `r1091.K14_unkept_never_cleared`

flush: leave the failure said after a later write succeeds

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K14_unkept_never_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`

Old text:

```
        self._unwritten = 0
        self.unkept = ""
```

New text:

```
        self._unwritten = 0
```

### `r1091.K15_reuse_uncounted`

fresh: count no reuse, so the screen says every read was made by this run

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K15_reuse_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`

Old text:

```
        self.reused += 1
```

New text:

```
        self.reused += 0
```

### `r1091.K1_age_never_expires`

_is_fresh: drop the upper bound, so a read is kept for ever and a changed release is planned from old tracks

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K1_age_never_expires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age
```

### `r1091.K2_future_is_fresh`

_is_fresh: drop the lower bound, so a read dated in the future is kept for as long as the clock is wrong

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K2_future_is_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return age < KEPT_FOR
```

### `r1091.K3_age_boundary`

_is_fresh: a read exactly the age old is still fresh

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K3_age_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age <= KEPT_FOR
```

### `r1091.K4_age_coefficient`

KEPT_FOR: eight days instead of seven, a realistic nearby value

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K4_age_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_first_build_says_its_reads_are_kept_for_the_apply_run`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_the_age_is_seven_days`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
KEPT_FOR = timedelta(days=7)
```

New text:

```
KEPT_FOR = timedelta(days=8)
```

### `r1091.K5_version_unchecked`

load: read a document of another version as if it were this one

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K5_version_unchecked`
- Moved: the same version check, now in the shared store's header read, compared against the store's own version, which is still 1
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 99, "label_id": "kompakt", "reads": {}}-it says version 99]`

Old text:

```
        if version != cls.version:
```

New text:

```
        if False:
```

### `r1091.K6_label_unchecked`

load: read another label's document as this label's reads

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K6_label_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "another", "reads": {}}-it names the label]`

Old text:

```
        if raw.get("label_id") != label_id:
```

New text:

```
        if False:
```

### `r1091.K7_gone_shape_unchecked`

_entry: accept a gone flag that is not a bool, so a string reads as gone

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K7_gone_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written8-says gone]`

Old text:

```
    if not isinstance(gone, bool):
```

New text:

```
    if False:
```

### `r1091.K8_year_shape_unchecked`

_entry: accept a year of any type, so a string or bool year reaches the plan

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K8_year_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written7-carries the year]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written9-carries the year]`

Old text:

```
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
```

New text:

```
    if False:
```

### `r1091.K9_track_shape_unchecked`

_entry: accept a malformed track entry

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K9_track_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written6-is malformed]`

Old text:

```
            not isinstance(track, Mapping)
            or not isinstance(track.get("id"), str)
            or not isinstance(track.get("available"), bool)
```

New text:

```
            not isinstance(track, Mapping)
```

### `u243.L7_kept_read_judged_blind`

KeptReads._is_fresh: a kept read without the tracks' words is reused and judged without them

- File: `src/cratekit/label/kept_reads.py`
- Source: `u243.json`, row `L7_kept_read_judged_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_label_playlists_kept.py`
- Collected: 74 against a baseline of 74
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[no-artist]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[no-title]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_missing_any_track_word_is_read_again[one-track-unnamed]`
  - `tests/test_label_tombstoned.py::test_a_kept_read_written_without_the_words_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR and kept.named
```

New text:

```
        return timedelta(0) <= age < KEPT_FOR
```

### `u308.L9_store_flushes_nothing`

kept_reads._Store.flush: answers held are never written

- File: `src/cratekit/label/kept_reads.py`
- Source: `u308.json`, row `L9_store_flushes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_kept_listing.py`, `tests/test_label_playlists.py`
- Collected: 138 against a baseline of 138
- Kills: 42 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_ceiling_stop_inside_discovery_keeps_every_search_it_finished`
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_failed_artist_read_in_discovery_still_refuses_rather_than_skipping`
  - `tests/test_label_kept_listing.py::test_a_failed_listing_is_not_kept`
  - `tests/test_label_kept_listing.py::test_a_kept_listing_valid_but_for_its_version_or_label_refuses[label_id-another-label-another-label]`
  - `tests/test_label_kept_listing.py::test_a_kept_listing_valid_but_for_its_version_or_label_refuses[version-2-version 2]`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed0]`
  - `tests/test_label_kept_listing.py::test_a_label_entry_that_changed_reads_the_kept_listing_as_empty[changed1]`
  - `tests/test_label_kept_listing.py::test_a_listing_just_inside_the_kept_life_is_still_answered`
  - `tests/test_label_kept_listing.py::test_a_listing_older_than_the_kept_life_is_asked_again`
  - `tests/test_label_kept_listing.py::test_a_listing_stopped_at_the_ceiling_continues_with_only_the_unread_part`
  - `tests/test_label_kept_listing.py::test_a_search_that_fails_on_a_continue_is_counted_so_the_line_stays_true`
  - `tests/test_label_kept_listing.py::test_a_second_label_sync_next_of_the_label_makes_no_provider_call`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        if self._unwritten:
            self._write(
```

New text:

```
        if False:
            self._write(
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

### `r1091.P10_unkept_screen_dropped`

_reads_said: say the reads are kept on the build gate's screen when they could not be written

- File: `src/cratekit/label/playlists_cli.py`
- Source: `r1091.json`, row `P10_unkept_screen_dropped`
- Moved: The same branch that says, for a run that reused nothing, that its reads could not be kept instead of saying they were kept; the unkept clause is now appended once at the end for both the reused and the fresh case, so this branch only names the reads and the mutation falls to the kept wording as before.
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
    elif reads.unkept:
        said = f"all {reads.read_now} release read(s) made by this run"
```

New text:

```
    elif False:
        said = f"all {reads.read_now} release read(s) made by this run"
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
- Collected: 523 against a baseline of 523
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
- Collected: 23216 against a baseline of 23216
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

### `u243.L12_suppressed_releases_unjudged`

playlists_cli.read_catalogue: the tracks of a release the tombstone suppressed are not judged, so a removed single stays on its year

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u243.json`, row `L12_suppressed_releases_unjudged`
- Moved: The same union of the suppressed releases' tombstoned tracks into the catalogue's tombstoned field; the grouped reads are now a map of LabelCatalogue fields, so the union is written onto that map before it is spread into the constructor.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 134 against a baseline of 134
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_removed_single_is_taken_off_though_its_release_is_suppressed`
  - `tests/test_label_tombstoned.py::test_hearing_never_merges_back_a_removed_single`

Old text:

```
    grouped["tombstoned"] = tuple(sorted({*grouped["tombstoned"], *held_back}))
```

New text:

```
    grouped["tombstoned"] = grouped["tombstoned"]
```

### `u243.L5_build_adds_a_tombstoned_track`

playlists_cli._group: a tombstoned track is not left out of its year, so a build adds it

- File: `src/cratekit/label/playlists_cli.py`
- Source: `u243.json`, row `L5_build_adds_a_tombstoned_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 134 against a baseline of 134
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
- Collected: 134 against a baseline of 134
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

### `r381-b.M12_add_legacy_any_name`

add takes the entry under the old fold whatever its display name

- File: `src/cratekit/label/registry.py`
- Source: `r381-b.json`, row `M12_add_legacy_any_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`

Old text:

```
                if legacy is not None and _name_key(legacy.name) == _name_key(name)
```

New text:

```
                if legacy is not None
```

### `r381.M10_by_id_no_follow`

by_id stops following the renamed map, so a frozen old identifier refuses label-unknown

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M10_by_id_no_follow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`

Old text:

```
        if found is None and label_id in self.renamed:
```

New text:

```
        if found is None and label_id in ():
```

### `r381.M11_add_ignores_legacy`

add keys on the new slug alone, so a collided label overwrites its neighbour

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M11_add_ignores_legacy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`

Old text:

```
                if legacy is not None and _name_key(legacy.name) == _name_key(name)
```

New text:

```
                if False
```

### `r381.M1_fold_only_slug`

Restore the fold only slug, the brief's named row: slug folds the raw name and transliterates nothing

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M1_fold_only_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Caf\xe9 del Mar-cafe-del-mar]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Stra\xdfe-strasse]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Sue\xf1o-sueno]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Suen\u0303o-sueno]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Sch\xf6n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Scho\u0308n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[\xc4\xd6\xdc Records-aeoeue-records]`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`
  - `tests/test_label_slug.py::test_re_adding_a_migrated_label_does_not_file_it_twice`

Old text:

```
    folded = _fold(stripped)
```

New text:

```
    folded = _fold(name)
```

### `r381.M2_no_umlaut_table`

Drop the umlaut and sharp s table, so NFKD alone turns Schön into schon

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M2_no_umlaut_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Stra\xdfe-strasse]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Sch\xf6n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Voll Scho\u0308n-voll-schoen]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[\xc4\xd6\xdc Records-aeoeue-records]`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`

Old text:

```
    composed = unicodedata.normalize("NFC", name).translate(_TRANSLITERATE)
```

New text:

```
    composed = unicodedata.normalize("NFC", name)
```

### `r381.M3_keep_combining_marks`

Keep the combining marks after NFKD, so they fold to hyphens as before

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M3_keep_combining_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_collision_leaves_the_old_identifier`
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Sue\xf1o-sueno]`
  - `tests/test_label_slug.py::test_a_slug_transliterates_before_it_folds[Suen\u0303o-sueno]`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_a_year_already_held_under_the_new_identifier_is_not_overwritten`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`
  - `tests/test_label_slug.py::test_re_adding_a_migrated_label_does_not_file_it_twice`

Old text:

```
        if not unicodedata.combining(char)
```

New text:

```
        if unicodedata.combining(char) or True
```

### `r381.M4_migrate_ignores_taken`

migrate moves an entry onto a slug another entry already holds

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M4_migrate_ignores_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_collision_leaves_the_old_identifier`
  - `tests/test_label_slug.py::test_re_adding_a_collided_label_updates_it_and_not_its_neighbour`

Old text:

```
        if new is None or new in taken:
```

New text:

```
        if new is None:
```

### `r381.M5_migrate_any_identifier`

migrate moves any entry whose slug differs, not only one the old fold produced

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M5_migrate_any_identifier`
- Moved: The _legacy_slug alias was the fold of the name and is now called as _fold; the mutation drops the old fold test as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_registry_survives_a_label_rename_without_orphaning_its_state`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries0]`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries1]`

Old text:

```
    if new == entry.label_id or entry.label_id != _fold(entry.name):

```

New text:

```
    if new == entry.label_id:

```

### `r381.M6_update_skips_move_write`

update writes nothing for a move when the mutator opts out, so load never persists a migration

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M6_update_skips_move_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`

Old text:

```
            if changed is not False or moved:
```

New text:

```
            if changed is not False:
```

### `r381.M7_load_never_migrates`

load returns the stored document without planning a move

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M7_load_never_migrates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`
  - `tests/test_label_slug.py::test_an_advance_of_another_label_carries_the_migrated_year_along`
  - `tests/test_label_slug.py::test_an_identifier_frozen_before_the_move_still_finds_its_label`

Old text:

```
        if not migrate(held)[1]:
            return held
```

New text:

```
        if True:
            return held
```

### `r381.M8_no_renamed_map`

The writer leaves the renamed map out, so no watermark can follow

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M8_no_renamed_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_migrated_label_keeps_its_watermark`
  - `tests/test_label_slug.py::test_a_stored_fold_only_identifier_migrates_on_load`

Old text:

```
        if renamed:
            # Only when something moved
```

New text:

```
        if False:
            # Only when something moved
```

### `r381.M9_live_renames_unfiltered`

live_renames keeps a move whose old identifier a new label holds again

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M9_live_renames_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_slug.py::test_a_stored_move_whose_old_identifier_is_held_is_not_followed`
  - `tests/test_label_slug.py::test_an_old_identifier_reused_by_a_new_label_stops_following`

Old text:

```
        return {old: new for old, new in self.renamed.items() if old not in self.labels}
```

New text:

```
        return dict(self.renamed)
```

### `u100-a.R1_slug_only_presence`

RegistryStore.adopt checks presence by slug alone, the R-381 hazard: a label held under sueno is filed again as sue-o

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R1_slug_only_presence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = Registry(labels=current).by_id(label_id)
```

### `u100-a.R2_no_presence_check`

RegistryStore.adopt never finds a label present, so every accepted name is written over the held entry

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R2_no_presence_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_carried_over_accented_label_is_not_filed_twice`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[case]`
  - `tests/test_label_registry_adopt.py::test_a_label_held_under_a_folded_name_is_reported_not_duplicated[padding]`
  - `tests/test_label_registry_adopt.py::test_an_accepted_label_is_added_once_and_a_second_run_adds_none`
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                if held is not None:
                    results.append(
```

New text:

```
                if False:
                    results.append(
```

### `u100-a.R3_presence_before_the_batch`

RegistryStore.adopt resolves against the file as loaded, not the entries this run already added, so two spellings in one run both add

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R3_presence_before_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_two_spellings_accepted_in_one_run_add_the_label_once`

Old text:

```
                held = Registry(labels=current).resolve(name)
```

New text:

```
                held = self.load().resolve(name)
```

### `u100-a.R4_slug_refusal_aborts`

a name that yields no identifier is no longer caught per name, so it aborts the whole adopt

- File: `src/cratekit/label/registry.py`
- Source: `u100-a.json`, row `R4_slug_refusal_aborts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 401 against a baseline of 401
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_a_name_with_no_identifier_fails_alone_and_the_rest_land`

Old text:

```
                except CratekitError as exc:
                    results.append(
```

New text:

```
                except KeyError as exc:
                    results.append(
```

### `u100-c.R5_adopt_always_writes_after_fix`

RegistryStore.adopt asks for a write even when it added nothing, re-measured after the fix round added its test

- File: `src/cratekit/label/registry.py`
- Source: `u100-c.json`, row `R5_adopt_always_writes_after_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_adopt.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_adopt.py::test_an_adopt_that_adds_nothing_does_not_rewrite_the_registry`

Old text:

```
            return any(result.added for result in results)
```

New text:

```
            return True
```

### `u341.G1_of_genre_any_genre`

Registry.of_genre: keep every label with any genre, so a group is every grouped label

- File: `src/cratekit/label/registry.py`
- Source: `u341.json`, row `G1_of_genre_any_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_declared_genre_no_label_carries_refuses_as_a_group_of_none`
  - `tests/test_label_sync_genre.py::test_a_genre_the_taxonomy_does_not_declare_refuses_naming_the_carried_genres`
  - `tests/test_label_sync_genre.py::test_a_genre_walk_nobody_can_answer_is_told_to_walk_the_group_again`
  - `tests/test_label_sync_genre.py::test_a_group_is_matched_folded_and_each_genre_named_once_as_first_spelled`
  - `tests/test_label_sync_genre.py::test_a_refusal_whose_taxonomy_cannot_be_read_still_names_the_carried_genres`
  - `tests/test_label_sync_genre.py::test_a_stop_on_the_last_label_of_its_genre_points_into_no_group`
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_asks_only_that_group_in_registry_order`
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_names_the_group_and_estimates_it_alone`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_asks_the_first_label_of_the_group`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_leaves_a_question_saved_outside_the_group`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_lists_that_group_alone`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_no_label_carries_refuses`
  - `tests/test_label_sync_genre.py::test_the_walk_after_quit_resumes_inside_the_group`

Old text:

```
            if entry.genre is not None and _name_key(entry.genre) == wanted
```

New text:

```
            if entry.genre is not None
```

### `u341.G2_of_genre_unfolded`

Registry.of_genre: match the genre as typed, so a group typed in another case is a group of none

- File: `src/cratekit/label/registry.py`
- Source: `u341.json`, row `G2_of_genre_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_group_is_matched_folded_and_each_genre_named_once_as_first_spelled`
  - `tests/test_label_sync_genre.py::test_registry_list_with_a_genre_lists_that_group_alone`
  - `tests/test_label_sync_genre.py::test_the_genre_is_matched_whatever_its_case`

Old text:

```
            if entry.genre is not None and _name_key(entry.genre) == wanted
```

New text:

```
            if entry.genre is not None and entry.genre == genre
```

### `u341.G3_genres_not_folded_once`

Registry.genres: key by the spelling, so a genre two labels spell in two cases is named twice

- File: `src/cratekit/label/registry.py`
- Source: `u341.json`, row `G3_genres_not_folded_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_genre.py`, `tests/modules/test_labels.py`
- Collected: 410 against a baseline of 410
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_group_is_matched_folded_and_each_genre_named_once_as_first_spelled`

Old text:

```
                held.setdefault(_name_key(entry.genre), entry.genre)
```

New text:

```
                held.setdefault(entry.genre, entry.genre)
```

### `u99-a.A10_edit_drops_match`

edit: write the passed match even when none was passed, so set --track-limit clears the needle

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A10_edit_drops_match`
- Moved: edit replaces the held entry with the checked changes, which leave out every field given as None; the mutation writes the passed match even when none was passed.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`

Old text:

```
            entry = replace(existing, **changes)

```

New text:

```
            entry = replace(existing, **{**changes, "match": match})

```

### `u99-a.A11_edit_drops_seeds`

edit: write the passed seeds even when none were passed, so set --track-limit clears the seeds

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A11_edit_drops_seeds`
- Moved: edit replaces the held entry with the checked changes; the mutation writes the passed seeds, or none, even when none were passed.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_set_changes_one_field_and_keeps_the_rest`

Old text:

```
            entry = replace(existing, **changes)

```

New text:

```
            entry = replace(existing, **{**changes, "seed_artists": seeds or ()})

```

### `u99-a.A12_edit_drops_limit`

edit: write the passed limit even when none was passed, so set --seed clears the limit

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A12_edit_drops_limit`
- Moved: edit replaces the held entry with the checked changes; the mutation writes the passed limit even when none was passed.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_set_seeds_replaces_the_list_and_keeps_the_limit`

Old text:

```
            entry = replace(existing, **changes)

```

New text:

```
            entry = replace(existing, **{**changes, "track_limit": track_limit})

```

### `u99-a.A13_by_name_unnormalized`

_folded: drop the NFC normalization, so a decomposed accented name resolves nothing

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A13_by_name_unnormalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return unicodedata.normalize("NFC", name.strip()).casefold()
```

New text:

```
    return name.strip().casefold()
```

### `u99-a.A1_blank_seed`

check_seed: drop the blank seed refusal, so a whitespace seed is stored as an empty name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A1_blank_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`

Old text:

```
    if not text:
        raise _field_invalid(
```

New text:

```
    if False:
        raise _field_invalid(
```

### `u99-a.A2_malformed_id_seed`

check_seed: drop the malformed id: refusal, so id:12a is stored and later searched for as a name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A2_malformed_id_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
```

New text:

```
    if False:
```

### `u99-a.A3_id_prefix_case`

check_seed: compare the id: prefix case sensitively, so ID:12 is stored as a name

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A3_id_prefix_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`

Old text:

```
    if text[:3].casefold() == "id:" and not _ID_SEED.fullmatch(text):
```

New text:

```
    if text[:3] == "id:" and not _ID_SEED.fullmatch(text):
```

### `u99-a.A4_id_digits_optional`

_ID_SEED: allow zero digits, so a bare id: is stored

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A4_id_digits_optional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
_ID_SEED = re.compile(r"id:[0-9]+")
```

New text:

```
_ID_SEED = re.compile(r"id:[0-9]*")
```

### `u99-a.A5_id_prefix_match`

check_seed: match the identifier as a prefix rather than whole, so id:12a is stored

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A5_id_prefix_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`

Old text:

```
not _ID_SEED.fullmatch(text):
```

New text:

```
not _ID_SEED.match(text):
```

### `u99-a.A7_add_unchecked_seeds`

add: store the seeds unchecked, so a malformed seed on add is written

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A7_add_unchecked_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_a_new_label_creates_no_entry`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[   ]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[ID:12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id: 12]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:-4]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:12a]`
  - `tests/test_label_registry_verbs.py::test_a_malformed_seed_on_add_refuses_and_writes_nothing[id:]`

Old text:

```
        seeds = _checked_seeds(seed_artists)

```

New text:

```
        seeds = tuple(seed_artists)

```

### `u99-a.A8_edit_unchecked_seeds`

edit: store the seeds unchecked, so a malformed seed on set is written

- File: `src/cratekit/label/registry.py`
- Source: `u99-a.json`, row `A8_edit_unchecked_seeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_a_malformed_id_seed_on_set_refuses_and_writes_nothing`

Old text:

```
        seeds = _checked_seeds(seed_artists) if seed_artists is not None else None
```

New text:

```
        seeds = tuple(seed_artists) if seed_artists is not None else None
```

### `u99-b.A6r_store_limit_floor`

check_track_limit: accept zero, measured again after the store level test the A6 zero bought

- File: `src/cratekit/label/registry.py`
- Source: `u99-b.json`, row `A6r_store_limit_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_registry_verbs.py::test_the_store_refuses_a_limit_below_one_from_a_python_caller[0]`

Old text:

```
or limit < 1:
```

New text:

```
or limit < 0:
```

### `u308.L5_extended_step_dropped`

review_common.extended: the step the review verbs add to a refusal is dropped

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L5_extended_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_artists.py`, `tests/test_label_sync_go.py`
- Collected: 247 against a baseline of 247
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_three_reads_failing_in_a_row_stop_the_run_and_say_what_was_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`

Old text:

```
    steps = (*cause.remediation.steps, step)
```

New text:

```
    steps = tuple(cause.remediation.steps)
```

### `u308.L6_ended_outcome_ignored`

review_common.ended: every review verb ends OK whatever outcome it reached

- File: `src/cratekit/label/review_common.py`
- Source: `u308.json`, row `L6_ended_outcome_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_genre_gate.py`, `tests/test_label_sync_go.py`
- Collected: 366 against a baseline of 366
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_approved.py::test_every_release_held_or_owned_is_a_no_op_that_does_not_claim_the_held_one`
  - `tests/test_label_approved.py::test_every_track_owned_is_a_no_op_and_writes_nothing`
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[accepted]`
  - `tests/test_label_artists.py::test_a_decided_item_reading_an_address_is_left_as_it_is[rejected]`
  - `tests/test_label_artists.py::test_a_queue_with_no_address_opens_no_catalogue`
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_release_the_provider_does_not_serve_is_counted_and_never_blanked`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[   ]`
  - `tests/test_label_artists.py::test_a_release_the_provider_names_no_artist_for_is_left_reading_what_it_read[]`
  - `tests/test_label_artists.py::test_an_artist_put_right_meanwhile_is_not_overwritten`
  - `tests/test_label_artists.py::test_an_empty_queue_is_a_no_op_that_opens_no_catalogue`
  - `tests/test_label_artists.py::test_an_item_whose_artist_is_a_name_is_not_asked_about`
  - `tests/test_label_genre_gate.py::test_a_held_release_returned_to_review_is_filed_and_not_held_again`
  - `tests/test_label_genre_gate.py::test_a_release_filed_before_the_sweep_had_a_gate_is_asked_about_at_approval`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        data={"checks": checks, "summary": summary}, outcome=outcome, warnings=warnings
```

New text:

```
        data={"checks": checks, "summary": summary}, outcome=Outcome.OK, warnings=warnings
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
- Moved: The handed library or the walk is chosen once at construction, a lambda keeping the walk lazy; the mutation ignores the handed library and always walks its own.
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_sweep_of_two_labels_walks_the_library_once`

Old text:

```
        self._library_of = library if library is not None else (

```

New text:

```
        self._library_of = library if False else (

```

### `r259.O1_no_tracks_guard`

A release the provider lists with no track reads as owned, since all over nothing is True

- File: `src/cratekit/label/sweep.py`
- Source: `r259.json`, row `O1_no_tracks_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 23216 against a baseline of 23216
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
- Collected: 23216 against a baseline of 23216
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
- Moved: list_recent now derives what it carries from the listings after the loop; the mutation carries no unread onto the source.
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
        self.unread = tuple(one for listing in lists for one in listing.unread)

```

New text:

```
        self.unread = ()

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

### `r704-a.S7_probe_unclassified`

the listing probe boundary hands the classifier a plain error, so a rate limit on a lazy listing attribute is permanent

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S7_probe_unclassified`
- Moved: The probe boundary is catalogue.translated, and the failure it raises is still built by _lookup_failure from the caught error; the mutation hands the classifier a plain error.
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
    )):
        listable = crawl.can_list(artist)

```

New text:

```
        f"that is not an empty catalogue",
        RuntimeError(),
    )):
        listable = crawl.can_list(artist)

```

### `r704-a.S8_crawl_unclassified`

the crawl boundary hands the classifier a plain error, the listing's spent ladder is permanent again

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S8_crawl_unclassified`
- Moved: The crawl boundary is catalogue.translated, the failure still built by _lookup_failure from the caught error; the mutation hands the classifier a plain error.
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
    )):

```

New text:

```
        f"({type(exc).__name__}: {exc}); that is not an empty catalogue",
        RuntimeError(),
    )):

```

### `r704-a.S9_resolve_unclassified`

the artist resolve boundary hands the classifier a plain error

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S9_resolve_unclassified`
- Moved: The artist resolve boundary is catalogue.translated, the failure still built by _lookup_failure from the caught error; the mutation hands the classifier a plain error.
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
            )):

```

New text:

```
                f"were never listed",
                RuntimeError(),
            )):

```

### `u107-a.S06_queued_also`

sweep.QueuedReleases: ignore the second container, so an asked release takes no place in the offer window

- File: `src/cratekit/label/sweep.py`
- Source: `u107-a.json`, row `S06_queued_also`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_genre_gate.py`, `tests/test_label_judge.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 933 against a baseline of 933
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

### `u238.M4_beyond_leaves_out_unchecked`

list_for_label: beyond is the label's own only, so the recorded round drops every unchecked release

- File: `src/cratekit/label/sweep.py`
- Source: `u238.json`, row `M4_beyond_leaves_out_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`, `tests/test_label_judge.py`
- Collected: 472 against a baseline of 472
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
- Collected: 472 against a baseline of 472
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

### `u277.M3_another_label_before_no_line`

line_reading order: rank a held release whose line names another label ahead of one with no line

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M3_another_label_before_no_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 309 against a baseline of 309
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

### `u277.M8_past_window_counts_other_labels`

_past_window: count a release whose line names another label as the label's own past the window (the shared reading, U238)

- File: `src/cratekit/label/sweep.py`
- Source: `u277.json`, row `M8_past_window_counts_other_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_offer_window.py`, `tests/test_label_sync.py`, `tests/test_label_genre_gate.py`
- Collected: 309 against a baseline of 309
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

### `u52-item-derivation.S5_dropped_never_accumulated`

Stop accumulating the dropped population in LabelSource.list_recent, so the refusal above can never see one

- File: `src/cratekit/label/sweep.py`
- Source: `u52-item-derivation.json`, row `S5_dropped_never_accumulated`
- Moved: list_recent now derives the dropped population from the listings after the loop; the mutation never accumulates it.
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
        self.dropped = tuple(drop for listing in lists for drop in listing.dropped)

```

New text:

```
        self.dropped = ()

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

### `r1114.M10_message_reworded_many`

_unlisted_cause: reword the many label message so it no longer says none could be read

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M10_message_reworded_many`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Moved: _skipped_check was used once and is inlined into _unasked; the fail status is the same word
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_closing_line_names_only_the_label_that_was_listed`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`
  - `tests/test_label_sync.py::test_next_with_one_label_skipped_and_the_next_asked_still_asks`

Old text:

```
        checks.append(_check(f"label.{entry.label_id}", "fail", said))
```

New text:

```
        checks.append(_check(f"label.{entry.label_id}", "info", said))
```

### `r1114.M16_remedy_line_dropped`

_next: refuse without the info line naming what to do, so the human rendering shows no remedy, the review's round one finding

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M16_remedy_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Moved: the nothing new branch _next and _walk shared moved into _unasked, which appends the name to the list _next hands it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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
            pass

```

### `r1114.M7_refusal_drops_the_lines`

_next: refuse without the run's checks as data, so the per label fail lines vanish from the refusal

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1114.json`, row `M7_refusal_drops_the_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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
- Moved: the origin keyword moved into the shared _refusal helper, so the retryable line no longer sits beside it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        retryable=True,

```

New text:

```
        retryable=False,

```

### `r515-operator.S8_short_of_keeps_zero`

Read a saved shortfall block back even when it withheld nothing

- File: `src/cratekit/label/sync_cli.py`
- Source: `r515-operator.json`, row `S8_short_of_keeps_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
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
- Moved: _counts says its clauses from a table of count and words; a zero count drops the shortfall as the false guard did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_short_release_is_counted_over_its_rows_and_the_question_says_the_shortfall`

Old text:

```
        (question.provider_withheld, f"; {question.provider_withheld} track(s) withheld by "
```

New text:

```
        (0, f"; {question.provider_withheld} track(s) withheld by "
```

### `u107-a.S03_marker_moves`

sync_cli.record_answer: keep the asked set as it was, so an answer does not move the marker and the same releases are asked again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S03_marker_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
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
- Moved: the same keyword passed to the same listing call, joined onto the run_id line when the call's arguments were grouped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
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
        run_id=tools.run_id, offered=asked,
```

New text:

```
        run_id=tools.run_id, offered=None,
```

### `u107-a.S07_gate_before_asking`

sync_cli._question_for: list the label with no genre gate, so a release the gate would hold reaches a question

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-a.json`, row `S07_gate_before_asking`
- Moved: the SweepGate keywords were joined onto fewer lines; dropping the gate is the same mutant
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`

Old text:

```
        gate=genre_gate.SweepGate(
            declared, tracks=reader.release_tracks, standing=genre_gate.StandingHolds(store),
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
- Collected: 95 against a baseline of 95
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
- Moved: the pick validation moved out of record_answer into _chosen, so the same test stands one level shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
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
- Moved: the choice of taken releases moved into _chosen, which returns this same comprehension one level shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
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
- Moved: the stop removal is now one conditional expression; the registry remove is the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_after_any_answer_a_second_run_asks_nothing_about_those_releases[stop]`
  - `tests/test_label_sync.py::test_stop_following_removes_the_label_and_records_no_download`
  - `tests/test_label_sync.py::test_stopping_after_two_of_five_labels_resumes_at_the_third`

Old text:

```
        removed = labels.RegistryStore().remove(entry.label_id) if answer == STOP else False
```

New text:

```
        removed = True if answer == STOP else False
```

### `u107-b.S13_take_accepts`

sync_cli._take: file a taken release and never record it accepted

- File: `src/cratekit/label/sync_cli.py`
- Source: `u107-b.json`, row `S13_take_accepts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 95 against a baseline of 95
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Moved: the pick refusal moved into _chosen and its remedy, the same words, is now one f-string on one line
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_pick_outside_the_question_names_next_label_for_its_identifiers`

Old text:

```
                f"take the identifiers from: crate label sync --next --label {entry.label_id}",
```

New text:

```
                "take the identifiers from: crate label sync --next",
```

### `u189.M13_walk_remedy_plain_next`

_walk: the unanswerable refusal's remedy names the plain --next and a placeholder label again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M13_walk_remedy_plain_next`
- Moved: the unanswerable refusal moved out of _walk into _unanswerable, so the same remedy lines stand shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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
- Collected: 205 against a baseline of 205
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

### `u189.M7_unknown_name_not_refused`

_next: resolve the name without refusing, so an unfollowed name walks every label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `M7_unknown_name_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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

### `u189.S1_saved_question_relisted`

_next, sample of the unit's existing guards: never reuse a saved question, so every --next lists the label again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S1_saved_question_relisted`
- Moved: _next reads the saved question through _pending, which holds the isinstance and releases test, so this is the same reuse guard
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_saved_question_is_printed_again_with_no_provider_call`
  - `tests/test_label_sync.py::test_next_label_leaves_another_labels_saved_question_exactly_as_it_was`
  - `tests/test_label_sync.py::test_next_label_prints_a_question_the_plain_next_saved_with_no_catalogue_call`
  - `tests/test_label_sync.py::test_next_label_prints_a_saved_question_again_with_no_catalogue_call`

Old text:

```
            if pending is not None:
                question = Question.from_json(pending)
```

New text:

```
            if False:
                question = Question.from_json(pending)
```

### `u189.S2_question_not_saved`

_next, sample of the unit's existing guards: print a new question without saving it, so no answer can apply to it

- File: `src/cratekit/label/sync_cli.py`
- Source: `u189.json`, row `S2_question_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
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
- Moved: the Question is built into a local before _Listed, so the same keyword stands four spaces shallower
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 321 against a baseline of 321
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
- Moved: Question.to_json writes its counts from the _QUESTION_COUNTS names in order; dropping the name drops the saved split as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 321 against a baseline of 321
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_an_unread_listing_still_says_so_beside_the_count_past_the_window`

Old text:

```
    "beyond", "beyond_unchecked", "unread", "withheld", "unjudged",
```

New text:

```
    "beyond", "unread", "withheld", "unjudged",
```

### `u238.M7_old_question_read_as_count`

Question.from_json: a question saved before the split reads none as unchecked, so 414 is said as the label's

- File: `src/cratekit/label/sync_cli.py`
- Source: `u238.json`, row `M7_old_question_read_as_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_sync_all.py`
- Collected: 321 against a baseline of 321
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
- Collected: 321 against a baseline of 321
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
- Collected: 321 against a baseline of 321
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

### `u278.M24_label_sync_not_narrowed`

label sync: ask and walk spend the reserve

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M24_label_sync_not_narrowed`
- Moved: label_sync returns the go first, so the reading narrowing runs for every other path without its own if
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_genre_walk_at_the_terminal_is_refused_over_its_group_alone`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_in_its_own_words_over_its_group_alone`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    provider_gate.reading(provider_gate.GateSettings.from_config(cfg))

```

New text:

```
    pass

```

### `u278.M25_sweep_never_refuses`

label sync: the estimate never refuses

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M25_sweep_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 385 against a baseline of 385
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_genre_walk_at_the_terminal_is_refused_over_its_group_alone`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_in_its_own_words_over_its_group_alone`
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if calls > left:
```

New text:

```
    if False:
```

### `u308.L1_record_lock_refusal_lost`

sync_cli.record_lock: a record that cannot be locked fails raw, not as the record's own refusal

- File: `src/cratekit/label/sync_cli.py`
- Source: `u308.json`, row `L1_record_lock_refusal_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_that_cannot_be_locked_refuses_rather_than_record_unlocked`

Old text:

```
    except config.ConfigLockUnavailable as exc:
```

New text:

```
    except ZeroDivisionError as exc:
```

### `u341.G10_asked_every_label`

_asked: name the group but return every followed label, so the walk and --next ask outside it

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G10_asked_every_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_genre_walk_nobody_can_answer_is_told_to_walk_the_group_again`
  - `tests/test_label_sync_genre.py::test_a_stop_on_the_last_label_of_its_genre_points_into_no_group`
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_asks_only_that_group_in_registry_order`
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_names_the_group_and_estimates_it_alone`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_asks_the_first_label_of_the_group`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_leaves_a_question_saved_outside_the_group`
  - `tests/test_label_sync_genre.py::test_the_walk_after_quit_resumes_inside_the_group`

Old text:

```
    return list(group), named, [_check("genre", "info", said)]
```

New text:

```
    return list(followed.labels.values()), named, [_check("genre", "info", said)]
```

### `u341.G11_walk_drops_genre`

label_sync: call the walk without the genre, so --genre at the terminal walks every label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G11_walk_drops_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_genre_asked_of_labels_that_carry_none_says_how_to_set_one`
  - `tests/test_label_sync_genre.py::test_a_genre_the_taxonomy_does_not_declare_refuses_naming_the_carried_genres`
  - `tests/test_label_sync_genre.py::test_a_genre_walk_nobody_can_answer_is_told_to_walk_the_group_again`
  - `tests/test_label_sync_genre.py::test_a_refusal_whose_taxonomy_cannot_be_read_still_names_the_carried_genres`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[ ]`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[!?]`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[Deep\x07House]`
  - `tests/test_label_sync_genre.py::test_a_shapeless_genre_refuses_naming_the_rule[aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa]`
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_asks_only_that_group_in_registry_order`
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_names_the_group_and_estimates_it_alone`
  - `tests/test_label_sync_genre.py::test_the_genre_is_matched_whatever_its_case`
  - `tests/test_label_sync_genre.py::test_the_resume_hint_quotes_a_genre_for_the_shell`
  - `tests/test_label_sync_genre.py::test_the_walk_after_quit_resumes_inside_the_group`

Old text:

```
    return _walk(ctx, cfg, PROMPTER(), args.genre)
```

New text:

```
    return _walk(ctx, cfg, PROMPTER())
```

### `u341.G12_next_drops_genre`

label_sync: call --next without the genre, so --next --genre asks the first label of any genre

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G12_next_drops_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_declared_genre_no_label_carries_refuses_as_a_group_of_none`
  - `tests/test_label_sync_genre.py::test_a_stop_on_the_last_label_of_its_genre_points_into_no_group`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_asks_the_first_label_of_the_group`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_leaves_a_question_saved_outside_the_group`
  - `tests/test_label_sync_genre.py::test_next_with_a_genre_whose_labels_have_nothing_new_says_so_of_the_group`

Old text:

```
        return _next(ctx, cfg, args.label, args.genre)
```

New text:

```
        return _next(ctx, cfg, args.label)
```

### `u341.G13_selection_guard_dropped`

label_sync: drop the refusal of --genre beside --go, --answer or --label, so the genre is silently ignored

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G13_selection_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_genre_beside_go_answer_or_one_label_refuses_as_a_selection[argv0]`
  - `tests/test_label_sync_genre.py::test_a_genre_beside_go_answer_or_one_label_refuses_as_a_selection[argv1]`
  - `tests/test_label_sync_genre.py::test_a_genre_beside_go_answer_or_one_label_refuses_as_a_selection[argv2]`
  - `tests/test_label_sync_genre.py::test_a_genre_beside_go_answer_or_one_label_refuses_as_a_selection[argv3]`
  - `tests/test_label_sync_genre.py::test_an_answer_with_a_genre_and_no_label_refuses_the_genre_first`

Old text:

```
    if args.genre is not None and (args.go or args.answer is not None or args.label is not None):
```

New text:

```
    if False and (args.go or args.answer is not None or args.label is not None):
```

### `u341.G14_selection_guard_without_label`

label_sync: leave --answer out of the selection refusal, so --answer --genre with no label is told to pass --label and then refused again

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G14_selection_guard_without_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_genre_beside_go_answer_or_one_label_refuses_as_a_selection[argv1]`
  - `tests/test_label_sync_genre.py::test_an_answer_with_a_genre_and_no_label_refuses_the_genre_first`

Old text:

```
    if args.genre is not None and (args.go or args.answer is not None or args.label is not None):
```

New text:

```
    if args.genre is not None and (args.go or args.label is not None):
```

### `u341.G15_resume_hint_unnamed`

_walk: the run stopped with quit is told to run label sync again with no genre, so it resumes outside the group

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G15_resume_hint_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_the_resume_hint_quotes_a_genre_for_the_shell`
  - `tests/test_label_sync_genre.py::test_the_walk_after_quit_resumes_inside_the_group`

Old text:

```
    again = "label sync" if named is None else f"label sync {_genre_flag(named)}"
```

New text:

```
    again = "label sync"
```

### `u341.G16_gate_shows_group_line`

_walk: let the line naming the group through to the gate, where it reads as an answer

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G16_gate_shows_group_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_walk_with_a_genre_asks_only_that_group_in_registry_order`

Old text:

```
        walk = [one["detail"] for one in checks if one["key"] not in (_ESTIMATE_KEY, _GENRE_KEY)]
```

New text:

```
        walk = [one["detail"] for one in checks if one["key"] != _ESTIMATE_KEY]
```

### `u341.G17_answer_hint_leaves_group`

_answer: never name the answered label's genre in the next hint, so a --next --genre run is pointed out of its group

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G17_answer_hint_leaves_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_every_answer_points_back_into_a_group_that_still_stands[all]`
  - `tests/test_label_sync_genre.py::test_every_answer_points_back_into_a_group_that_still_stands[not-now]`
  - `tests/test_label_sync_genre.py::test_every_answer_points_back_into_a_group_that_still_stands[pick]`
  - `tests/test_label_sync_genre.py::test_every_answer_points_back_into_a_group_that_still_stands[stop]`

Old text:

```
    group = "" if not standing else (
```

New text:

```
    group = "" if True else (
```

### `u341.G18_unanswerable_hint_leaves_group`

_walk: the refusal of a genre walk nobody can answer is told to run label sync with no genre

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G18_unanswerable_hint_leaves_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_genre_walk_nobody_can_answer_is_told_to_walk_the_group_again`

Old text:

```
                raise _unanswerable(entry, answered, exc, named) from exc
```

New text:

```
                raise _unanswerable(entry, answered, exc) from exc
```

### `u341.G19_budget_wording_unnamed`

_sweep_check: the budget refusal of a genre walk speaks of every followed label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G19_budget_wording_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_provider_budget.py`, `tests/modules/test_labels.py`
- Collected: 377 against a baseline of 377
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_genre_walk_at_the_terminal_is_refused_over_its_group_alone`
  - `tests/test_provider_budget.py::test_a_genre_walk_is_refused_in_its_own_words_over_its_group_alone`

Old text:

```
    return "the followed labels" if genre is None else f"the labels of genre {genre!r}"
```

New text:

```
    return "the followed labels"
```

### `u341.G20_hint_into_a_dissolved_group`

_answer: name the label's genre in the next hint even when the answer stopped the group's last label

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G20_hint_into_a_dissolved_group`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_a_stop_on_the_last_label_of_its_genre_points_into_no_group`

Old text:

```
    standing = entry.genre is not None and labels.RegistryStore().load().of_genre(entry.genre)
```

New text:

```
    standing = entry.genre is not None
```

### `u341.G21_hint_quoted_as_repr`

_genre_flag: quote the genre in a hint as Python repr, which a shell cannot read for an apostrophe

- File: `src/cratekit/label/sync_cli.py`
- Source: `u341.json`, row `G21_hint_quoted_as_repr`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_genre.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/modules/test_labels.py`
- Collected: 425 against a baseline of 425
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_genre.py::test_the_resume_hint_quotes_a_genre_for_the_shell`

Old text:

```
    return shlex.join(["--genre", genre])
```

New text:

```
    return f"--genre {genre!r}"
```

### `r1313.C1_catalogue_failure_alone`

_gone: read the 404 off the failure alone, as before R-1313, so a release answered with a 404 page climbs the ladder and fails as an outage

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C1_catalogue_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.C2_catalogue_name_on_any_link`

_gone: read a not found class name on any link, so a parse failure met while handling a not found reads the release as gone

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C2_catalogue_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if any("notfound" in type(one).__name__.lower() for one, _ in provider_session.failure_links(exc)):
        return True
    return answered_not_found(exc)
```

### `r261.D1_discovery_record`

_discover skips a failed listing without recording it, which is R-393 as it was

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D1_discovery_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`

Old text:

```
                unread.append(
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
```

New text:

```
                (
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
```

### `r261.D2_transient_class`

_discover marks every listing failure transient, a listing that cannot page included

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D2_transient_class`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`

Old text:

```
                        transient=not isinstance(
```

New text:

```
                        transient=True or not isinstance(
```

### `r261.D3_held_guard`

_discover records a held artist the roster reads again (the review finding)

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D3_held_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`

Old text:

```
                if str(getattr(artist, "id", "") or artist_id) in held_ids:
                    continue
```

New text:

```
                if str(getattr(artist, "id", "") or artist_id) in ():
                    continue
```

### `r261.R2_roster_keeps_discovery`

LabelRoster.unread keeps only its own missing listings and loses what discovery handed in

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `R2_roster_keeps_discovery`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`

Old text:

```
        self.unread = (*unread, *missing)
```

New text:

```
        self.unread = (*missing,)
```

### `r351.A2_unresolved_seed_skipped`

crawl the seeds that resolved and skip the one that did not

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A2_unresolved_seed_skipped`
- Moved: The unresolved seed sentences are built by one comprehension; the mutation refuses only when nothing resolved, as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`

Old text:

```
        if unresolved:
            bits = [

```

New text:

```
        if unresolved and not artists:
            bits = [

```

### `r351.A3_empty_roster_returned`

return an empty roster for a label nothing resolved

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A3_empty_roster_returned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolvable_label_raises_and_never_returns_none`
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`
  - `tests/test_label_tidal_catalogue.py::test_the_absence_contract_holds_through_the_sweep`

Old text:

```
        if not artists:
            raise LabelUnresolvable(
```

New text:

```
        if not artists:
            return LabelRoster([])
            raise LabelUnresolvable(
```

### `r351.A5_ambiguity_takes_first`

take the first of two artists named exactly the same

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `A5_ambiguity_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_colliding_name_seed_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_two_artists_named_exactly_the_label_refuse_rather_than_guess`

Old text:

```
        if len(distinct) > 1:
```

New text:

```
        if len(distinct) > 2:
```

### `r351.G10_identifier_message_says_named`

an unresolved identifier is reported as a name the provider does not carry

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G10_identifier_message_says_named`
- Moved: The identifier or name sentence is one conditional in the comprehension; the mutation always says named.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`

Old text:

```
                f"no artist with identifier {seed!r}"
                if seed_identifier(seed) is not None
                else f"no artist named exactly {seed!r}"

```

New text:

```
                f"no artist named exactly {seed!r}"

```

### `r351.G3_unresolved_id_skipped`

a seed that does not resolve is skipped rather than refusing the label

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G3_unresolved_id_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_does_not_resolve_refuses_the_label_rather_than_narrowing_it`
  - `tests/test_label_tidal_catalogue.py::test_an_id_lookup_that_returns_none_is_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_id_seed_refuses_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolved_name_seed_refuses_even_when_discovery_would_find_albums`
  - `tests/test_label_tidal_catalogue.py::test_the_client_object_not_found_is_an_unresolved_id_seed`

Old text:

```
            if artist is None:
                unresolved.append(seed)

```

New text:

```
            if artist is None:
                continue

```

### `r351.G4_any_remainder_is_an_id`

treat anything after id: as an identifier, including a name

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G4_any_remainder_is_an_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_seed_that_is_not_digits_after_the_prefix_is_still_a_name`

Old text:

```
_ID_SEED = re.compile(r"^id:(\d+)$")

```

New text:

```
_ID_SEED = re.compile(r"^id:(.+)$")

```

### `r351.G5_except_everything`

a provider outage looking up an identifier is read as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G5_except_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_outage_looking_up_an_id_seed_is_not_an_unresolved_seed`
  - `tests/test_label_tidal_catalogue.py::test_a_session_dead_during_discovery_refuses_the_label`

Old text:

```
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:
            # Bare LookupError is the fake's not found. KeyError and IndexError
            # are subclasses, and those are parse failures, not a missing id.
            if type(exc) is not LookupError:
                raise
            return None

```

New text:

```
        except Exception:
            return None

```

### `r351.G7_drop_object_not_found`

the live client's ObjectNotFound is no longer treated as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G7_drop_object_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_the_client_object_not_found_is_an_unresolved_id_seed`

Old text:

```
        except tidalapi.exceptions.ObjectNotFound:
            return None
        except LookupError as exc:

```

New text:

```
        except LookupError as exc:

```

### `r351.G8_id_prefix_case_insensitive`

ID:99 is treated as an identifier, against the locked id:<digits> shape

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G8_id_prefix_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_uppercase_id_prefix_is_still_a_name_seed`

Old text:

```
_ID_SEED = re.compile(r"^id:(\d+)$")

```

New text:

```
_ID_SEED = re.compile(r"^id:(\d+)$", re.IGNORECASE)

```

### `r351.G9_all_lookuperror_is_absence`

KeyError and IndexError from the identifier lookup are read as a missing seed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r351.json`, row `G9_all_lookuperror_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_key_error_looking_up_an_id_seed_is_not_an_unresolved_seed`

Old text:

```
            if type(exc) is not LookupError:
                raise
            return None

```

New text:

```
            return None

```

### `r352.A2_empty_roster_returned`

return an empty roster for a label nothing resolved

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `A2_empty_roster_returned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`
  - `tests/test_label_tidal_catalogue.py::test_an_unresolvable_label_raises_and_never_returns_none`
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`
  - `tests/test_label_tidal_catalogue.py::test_the_absence_contract_holds_through_the_sweep`

Old text:

```
        if not artists:
            raise LabelUnresolvable(

```

New text:

```
        if False and not artists:
            raise LabelUnresolvable(

```

### `r352.G10_no_collaborator_enqueue`

BFS does not enqueue credited artists from listed matching releases

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G10_no_collaborator_enqueue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_enqueues_collaborators_from_listed_matching_releases`

Old text:

```
            for release in releases:
                if _credits_label(release, needle):
                    for identity in _credited_ids(release):
                        enqueue(identity)

```

New text:

```
            for release in releases:
                if _credits_label(release, needle):
                    pass

```

### `r352.G11_discovered_not_added`

credited artists are walked but never appended to the roster

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G11_discovered_not_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 10 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_credit_starting_with_p_or_c_is_resolved_whole`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered`
  - `tests/test_label_tidal_catalogue.py::test_discovery_enqueues_collaborators_from_listed_matching_releases`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`
  - `tests/test_label_tidal_catalogue.py::test_discovery_matches_copyright_against_the_entry_match_needle`
  - `tests/test_label_tidal_catalogue.py::test_discovery_runs_when_the_label_already_has_an_artist_page`

Old text:

```
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)

```

New text:

```
            if identity not in held_ids:
                held_ids.add(identity)

```

### `r352.G13_duplicate_roster_member`

a discovered artist already on the roster is appended again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G13_duplicate_roster_member`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_discovered_artist_already_on_the_roster_is_not_added_twice`

Old text:

```
            if identity not in held_ids:
                discovered.append(artist)
                held_ids.add(identity)

```

New text:

```
            discovered.append(artist)
            held_ids.add(identity)

```

### `r352.G2_skip_when_roster_nonempty`

discovery does not run when the label already has an artist page

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G2_skip_when_roster_nonempty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_an_authentication_error_on_album_search_still_refuses_the_label`
  - `tests/test_label_tidal_catalogue.py::test_discovery_runs_when_the_label_already_has_an_artist_page`

Old text:

```
        needle = entry.match or entry.name
        seen: set[str] = set()

```

New text:

```
        if held:
            return []
        needle = entry.match or entry.name
        seen: set[str] = set()

```

### `r352.G4_empty_message_omits_discovery`

an empty roster still says only that the label names no seed artists

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G4_empty_message_omits_discovery`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_that_finds_only_copyright_mismatches_still_refuses`

Old text:

```
                f"the provider has no artist named exactly {entry.name!r}, the "
                f"label names no seed artists, and discovery found nothing"

```

New text:

```
                f"the provider has no artist named exactly {entry.name!r} and the "
                f"label names no seed artists to crawl instead"

```

### `r352.G5_compilation_range_shrunk`

numbered compilation searches stop at 001

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G5_compilation_range_shrunk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`

Old text:

```
COMPILATION_RANGE = range(1, 80)

```

New text:

```
COMPILATION_RANGE = range(1, 2)

```

### `r352.G6_name_query_only`

discovery searches the bare label name and no numbered compilations

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G6_name_query_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_compilation_returned_only_for_a_numbered_query_is_consumed`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_on_one_album_query_does_not_discard_the_own_page`
  - `tests/test_label_tidal_catalogue.py::test_numbered_compilation_queries_are_the_production_range`

Old text:

```
    return (name, *(f"{name} {number:03d}" for number in COMPILATION_RANGE))

```

New text:

```
    return (name,)

```

### `r352.G7_ignore_match_needle`

copyright match uses the display name and ignores entry.match

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r352.json`, row `G7_ignore_match_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_discovery_matches_copyright_against_the_entry_match_needle`

Old text:

```
        needle = entry.match or entry.name

```

New text:

```
        needle = entry.name

```

### `r504-a.A1_lt_to_le`

Adapter compares with <= instead of <, so a listing that reached its count raises a shortfall of zero

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A1_lt_to_le`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_complete_hearts_listing_reports_no_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_hearts_listing_pages_to_the_declared_total_through_the_listing`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if declared is not None and len(rows) <= declared:
```

### `r504-a.A2_lt_to_gt`

Adapter compares the wrong way round, so a short listing returns and a long one raises

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A2_lt_to_gt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_longer_than_its_count_is_not_a_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if declared is not None and len(rows) > declared:
```

### `r504-a.A3_no_none_guard`

Adapter drops the guard for a count the provider did not publish

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A3_no_none_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[-1]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[0]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[None]`

Old text:

```
        if declared is not None and len(rows) < declared:
```

New text:

```
        if len(rows) < declared:
```

### `r504-a.A4_no_raise`

Adapter never raises the shortfall, which is the pre R-504 behaviour

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r504-a.json`, row `A4_no_raise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
            raise HeartsShortfall(rows, declared)
```

New text:

```
            pass
```

### `r515-operator.S7_adapter_no_count`

The release adapter ignores the album's num_tracks

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r515-operator.json`, row `S7_adapter_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`

Old text:

```
        short = ListingShortfall.of(tracks, getattr(album, "num_tracks", None))
```

New text:

```
        short = None
```

### `r705-b.S9_playlist_read_wraps_the_park`

the playlist read wraps the park into an unresolvable playlist again

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r705-b.json`, row `S9_playlist_read_wraps_the_park`
- Moved: The playlist read boundary is catalogue.translated, whose default passing type is CratekitError, the park; the mutation passes nothing through, so the park is wrapped as an unresolvable playlist.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_playlist_read_lets_the_park_through`

Old text:

```
        )):
            playlist = self._session.playlist(identifier)

```

New text:

```
        ), passing=()):
            playlist = self._session.playlist(identifier)

```

### `r840-c.C3_the_adapter_reads_a_name`

TidalCatalogue.release_artist: answer with the text of the album's artist object, which is its address, the defect R-379 named

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r840-c.json`, row `C3_the_adapter_reads_a_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limited_artist_read_waits_and_is_asked_again`
  - `tests/test_label_tidal_catalogue.py::test_a_releases_artist_is_its_name_and_never_the_objects_address`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`
  - `tests/test_label_tidal_catalogue.py::test_the_sweep_files_the_name_the_artist_read_returns`

Old text:

```
        return artist_name(self._album(release_id))
```

New text:

```
        return str(getattr(self._album(release_id), "artist", "") or "")
```

### `r879-b.T2_offset_not_sent`

TidalCatalogue.search_tracks: send offset 0 to the client whatever page was asked

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r879-b.json`, row `T2_offset_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_track_search_asks_for_the_page_its_offset_names`

Old text:

```
                query, models=[tidalapi.media.Track], limit=limit, offset=offset
```

New text:

```
                query, models=[tidalapi.media.Track], limit=limit, offset=0
```

### `r888.R1_roster_serves_one_listing`

LabelRoster.held: the roster answers its albums for every listing, so its singles are never read

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r888.json`, row `R1_roster_serves_one_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory`

Old text:

```
        return self._listed.get(method)
```

New text:

```
        return self._listed.get("get_albums")
```

### `u217.A2_roster_lists_now`

_roster: hand the roster no lister, so every member is paged again after discovery

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u217.json`, row `A2_roster_lists_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_kept_listing.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 212 against a baseline of 212
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_kept_listing.py::test_a_continue_stopped_inside_an_artist_listing_still_costs_less_than_fresh`
  - `tests/test_label_kept_listing.py::test_a_kept_seed_the_provider_no_longer_has_is_unread_not_empty`
  - `tests/test_label_kept_listing.py::test_a_listing_the_client_does_not_expose_stays_unread_on_every_run`
  - `tests/test_label_kept_listing.py::test_a_second_listing_of_the_same_label_asks_the_provider_nothing`
  - `tests/test_label_kept_listing.py::test_label_playlists_after_a_sync_listing_asks_no_listing`
  - `tests/test_label_kept_listing.py::test_the_first_listing_pages_each_discovered_artist_once`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`

Old text:

```
            lister=lambda artist, method, missing: self._listed(kept, artist, method, missing),
```

New text:

```
            lister=None,
```

### `u261.O1_catalogue_drops_the_app`

open_catalogue: build the catalogue without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u261.json`, row `O1_catalogue_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 270 against a baseline of 270
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
        catalogue=held.app,
```

New text:

```
        catalogue=None,
```

### `u62.A1_missing_playlist_returns_none`

Return None for a playlist the client returned nothing for

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A1_missing_playlist_returns_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_playlist_the_client_returns_nothing_for_raises_too`

Old text:

```
        if playlist is None:
            raise PlaylistUnresolvable(
```

New text:

```
        if playlist is None:
            return None
            raise PlaylistUnresolvable(
```

### `u62.A4_first_hit_not_exact`

Take any hit the search returned rather than an exact name

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A4_first_hit_not_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_near_name_is_not_the_label`

Old text:

```
            if label_verify.fold_label(str(getattr(artist, "name", "") or "")) == wanted
```

New text:

```
            if label_verify.fold_label(str(getattr(artist, "name", "") or ""))
```

### `u62.A6_no_reread_for_missing_copyright`

Judge a release with no copyright line unconfirmed instead of re-reading it

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A6_no_reread_for_missing_copyright`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_confirms_from_its_own_copyright_line_or_a_re_read`

Old text:

```
        if not resolved and identity:
```

New text:

```
        if not resolved and not identity:
```

### `u62.A7_any_search_hit_confirms`

Confirm a harvested label on any album with a copyright line

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u62.json`, row `A7_any_search_hit_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_harvested_name_is_confirmed_only_by_a_matching_copyright_line`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
            if resolved and label_verify.labels_match(name, resolved):
```

New text:

```
            if resolved:
```

### `u70.A1_no_favourites_refused`

A client exposing no favourites is not refused by name, so the read fails as an attribute error

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u70.json`, row `A1_no_favourites_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_client_that_exposes_no_favourites_refuses_rather_than_holding_no_hearts`

Old text:

```
        if getattr(user, "favorites", None) is None:
```

New text:

```
        if False:
```

### `u75-c.C1_gone_is_never_retried`

Stop classifying a not found answer first, so a withdrawn release climbs the whole retry ladder

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C1_gone_is_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_404_status_is_gone_whatever_the_class_is_called`
  - `tests/test_label_tidal_catalogue.py::test_a_gone_release_has_no_artist_to_read_and_is_asked_about_once`
  - `tests/test_label_tidal_catalogue.py::test_a_release_that_is_gone_raises_at_once_and_is_never_retried`
  - `tests/test_label_tidal_catalogue.py::test_the_adapter_and_the_verb_meet_over_a_gone_release`

Old text:

```
                if _gone(exc):
                    return _GONE
                raise
```

New text:

```
                raise
```

### `u75-c.C5_none_album_raises`

Let a client that returned nothing for a release through to the listing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C5_none_album_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_the_client_returns_nothing_for_raises_too`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_read_the_client_returns_nothing_for_raises_too`

Old text:

```
        if album is _GONE or album is None:
```

New text:

```
        if album is _GONE:
```

### `u75-c.C7_tracks_through_the_paging_wrapper`

List the tracks with one direct call instead of the paging wrapper, which serves one page

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u75-c.json`, row `C7_tracks_through_the_paging_wrapper`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_release_is_paged_to_its_declared_count_and_carries_its_year`
  - `tests/test_label_tidal_catalogue.py::test_a_short_window_in_the_middle_of_a_release_does_not_end_it`
  - `tests/test_label_tidal_catalogue.py::test_the_adapter_pages_nothing_by_hand`

Old text:

```
        tracks = listing.playlist_tracks(album, shape="release_tracks", sleep=_pause)
```

New text:

```
        tracks = album.tracks()
```

### `u78-c.D2_blank_isrc`

A blank ISRC is sent to the provider

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u78-c.json`, row `D2_blank_isrc`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[   ]`
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[None]`
  - `tests/test_label_tidal_catalogue.py::test_no_isrc_is_refused_before_the_provider_is_asked[]`

Old text:

```
        if not wanted:
            raise ValueError("no ISRC was given to look up")
```

New text:

```
(empty)
```

### `u78-c.D3_no_lookup_method`

A client with no ISRC lookup climbs the whole ladder before failing

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u78-c.json`, row `D3_no_lookup_method`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_client_with_no_isrc_lookup_refuses_at_once_and_never_climbs_the_ladder`

Old text:

```
        if not callable(lookup):
            # A client without the method cannot be asked, and waiting on the
            # ladder cannot grow one.
            raise LookupError("the provider client exposes no ISRC lookup")
```

New text:

```
(empty)
```

### `u79-c.D1_search_shape_read_as_empty`

A search answer with no track listing is read as no candidate

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u79-c.json`, row `D1_search_shape_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`
- Collected: 174 against a baseline of 174
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_search_answer_with_no_track_listing_is_raised_at_once_and_is_not_empty`

Old text:

```
        if not present:
            raise LookupError("the provider's search answer carries no track listing")
```

New text:

```
        if False:
            raise LookupError("the provider's search answer carries no track listing")
```

### `u243.L1_companion_not_asked`

Tombstoned: the uncredited companion kind is not asked

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L1_companion_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_the_companion_of_a_credited_deletion_answers_for_the_provider_spelling`

Old text:

```
        for kind in (tombstone.KIND_VERSION, tombstone.KIND_VERSION_UNCREDITED):
```

New text:

```
        for kind in (tombstone.KIND_VERSION,):
```

### `u243.L2_revoked_tombstones_count`

Tombstoned: the snapshot includes revoked records, so a lifted deletion still takes the track off

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L2_revoked_tombstones_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_revoked_tombstone_takes_nothing_off`

Old text:

```
                record.suppression_id for record in store.suppressions()
```

New text:

```
                record.suppression_id for record in store.suppressions(include_revoked=True)
```

### `u243.L3_artists_joined_with_ampersand`

track_artist: the billed artists are joined by an ampersand, not as the downloader tags them

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L3_artists_joined_with_ampersand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 134 against a baseline of 134
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_the_track_words_are_read_as_the_downloader_tags_them`

Old text:

```
        return ", ".join(names)
```

New text:

```
        return " & ".join(names)
```

### `u243.L4_title_without_version`

track_title: the bare name is read before the full name, so the version is dropped

- File: `src/cratekit/label/tombstoned.py`
- Source: `u243.json`, row `L4_title_without_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`, `tests/test_label_playlists.py`
- Collected: 134 against a baseline of 134
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_kept_read_judges_a_track_by_the_words_it_kept`
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_a_tombstone_of_another_version_takes_nothing_off[Label Act-Track t5]`
  - `tests/test_label_tombstoned.py::test_the_track_words_are_read_as_the_downloader_tags_them`

Old text:

```
    for attribute in ("full_name", "name", "title"):
```

New text:

```
    for attribute in ("name", "full_name", "title"):
```

