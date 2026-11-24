# Mutation table: u335-before-01

Measured by `scripts/mutate.py` on 2026-11-24 05:01 UTC, branch `HEAD` at `b41c698d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 278.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:01 UTC for commit `b41c698da363`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 60, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u251.W1_drop_worksteal` | `pyproject.toml` | maintainer | 3 file(s) | 204 | 3 | killed |
| `u251.W2_dist_load` | `pyproject.toml` | maintainer | 3 file(s) | 204 | 2 | killed |
| `u251.W3_driver_strips_the_distribution` | `scripts/mutate.py` | maintainer | 2 file(s) | 146 | 2 | killed |
| `u197.M7_display_name` | `src/cratekit/_vendor/downloader/__init__.py` | user | 1 file(s) | 44 | 7 | killed |
| `u197.M10_adoption_copies` | `src/cratekit/_vendor/downloader/helper/path.py` | user | 1 file(s) | 44 | 3 | killed |
| `u197.M11_failed_move_fallback` | `src/cratekit/_vendor/downloader/helper/path.py` | user | 1 file(s) | 44 | 2 | killed |
| `u197.M12_lost_race_fallback` | `src/cratekit/_vendor/downloader/helper/path.py` | user | 1 file(s) | 44 | 2 | killed |
| `u197.M13_adopt_only_a_directory` | `src/cratekit/_vendor/downloader/helper/path.py` | user | 1 file(s) | 44 | 2 | killed |
| `u197.M8_adoption_off` | `src/cratekit/_vendor/downloader/helper/path.py` | user | 1 file(s) | 44 | 3 | killed |
| `r1115.M1_failed_needs_a_failure` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 1 | killed |
| `r1115.M2_every_failure_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 5 | killed |
| `r1115.M3_nothing_left_to_run` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 1 | killed |
| `r1115.M4_retryable_is_not_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 4 | killed |
| `r1115.M5_declined_is_refused` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M6_landed_needs_a_track` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 3 | killed |
| `r1115.M7_done_counts_done` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 8 | killed |
| `r1115.M8_failed_names_the_failures` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 369 | 2 | killed |
| `u108-c.G25_drive_maps_ending` | `src/cratekit/acquire/cli.py` | user | 7 file(s) | 476 | 31 | killed |
| `u169.A2_any_permanent_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 7 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `u169.A4_no_declined_warning` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 4 | killed |
| `u274.C1_worker_names_no_drive` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 450 | 17 | killed |
| `u206-b.M2b_disabled_recall_composite` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1131 | 8 | killed |
| `u206.M13_write_without_merge` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1131 | 5 | killed |
| `u206.M1_recall_never_hits` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1131 | 19 | killed |
| `u77-c.C1_manifest_version` | `src/cratekit/acquire/listdoc.py` | user | 6 file(s) | 254 | 2 | killed |
| `u77-c.C3_not_a_manifest` | `src/cratekit/acquire/listdoc.py` | user | 6 file(s) | 254 | 3 | killed |
| `r1360.J3_prefix_always_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 4 | killed |
| `r1360.J4_prefix_uncounted_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 2 | killed |
| `r1360.W11_offset_dropped` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 19 | killed |
| `r1360.W13_declared_unread` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 24 | killed |
| `r1360.W1_no_walk` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 24 | killed |
| `r1360.W2_walk_no_overlap` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 19 | killed |
| `r1360.W7_full_page_ends` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 10 | killed |
| `r1360.W8_overlap_kept` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 25 | killed |
| `u226.M1_equal_not_agreed` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 785 | 78 | killed |
| `u226.M4_prefix_as_subset` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 785 | 3 | killed |
| `u252.L1_ladder_exponent` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L2_ladder_rungs` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L3_ladder_ceiling_off_by_one` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L4_ladder_cap` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L5_ladder_base` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L6_no_ladder` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u265.M4_query_not_sorted` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2712 | 42 | killed |
| `u265.M5_hit_named_by_its_sorted_form` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2712 | 61 | killed |
| `u305.M4_index_library_not_reexported` | `src/cratekit/acquire/match.py` | maintainer | 3 file(s) | 709 | 301 | killed |
| `u305.M1_recorded_recording_swapped` | `src/cratekit/acquire/match_identity.py` | user | 2 file(s) | 642 | 71 | killed |
| `u249.M01_path_alone` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 7 | killed |
| `u249.M02_size_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 2 | killed |
| `u249.M03_mtime_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M04_ctime_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M05_inode_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M06_device_out_of_stamp` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M07_size_not_stat` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 2 | killed |
| `u249.M08_template_out_of_key` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M09_no_window` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 4 | killed |
| `u249.M10_window_halved` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 3 | killed |
| `u249.M11_window_boundary` | `src/cratekit/acquire/match_library.py` | maintainer | 4 file(s) | 780 | 1 | killed |
| `u249.M12_moment_after_read` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u249.M13_failed_read_remembered` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 3 | killed |
| `u249.M14_unstated_remembered_never` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 11 | killed |
| `u249.M20_reset_forgets_nothing` | `src/cratekit/acquire/match_library.py` | maintainer | 4 file(s) | 780 | 6 | killed |
| `u249.M20a_failed_read_keeps_old_entry` | `src/cratekit/acquire/match_library.py` | user | 4 file(s) | 780 | 1 | killed |
| `u265.M6_cache_misaligned` | `src/cratekit/acquire/match_library.py` | user | 24 file(s) | 2712 | 15 | killed |
| `u213.M5_listed_names_artist` | `src/cratekit/acquire/match_list.py` | user | 3 file(s) | 726 | 3 | killed |
| `r1694.S2_tolerance_always` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 209 | 3 | killed |
| `r1694.S4_failures_no_credential` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 209 | 8 | killed |
| `r1694.S5_failures_no_cratekit` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 209 | 2 | killed |
| `r1694.S6_failures_no_oserror` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 209 | 1 | killed |
| `u274.P1_gone_never` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 1 | killed |
| `u274.P4_sweep_live` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 7 | killed |
| `u274.P5_sweep_not_dir` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 2 | killed |
| `u274.P6_sweep_other_account` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 1 | killed |
| `u274.P7_no_sweep` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 1 | killed |
| `u274.P8_captured_always` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 3 | killed |
| `u274.P9_captured_nothing` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 6 | killed |
| `r1694.V1_drive_failures_narrowed` | `src/cratekit/acquire/vendored.py` | user | 3 file(s) | 130 | 2 | killed |
| `u274.V11_defect_swallowed` | `src/cratekit/acquire/vendored.py` | maintainer | 6 file(s) | 450 | 1 | killed |
| `u274.V12_scope_per_invocation` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 16 | killed |
| `u274.V1_refusal_forgotten` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 4 | killed |
| `u274.V2_login_refusal_unrecorded` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 2 | killed |
| `u274.V5_source_per_track` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 14 | killed |
| `u274.V6_no_rebind` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 1 | killed |
| `u274.V8_atmos_stored` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 1 | killed |
| `u274.V9_no_capture` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 450 | 7 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 86 | killed |
| `u339.M25_record_union` | `src/cratekit/adopt/genre_moves.py` | user | 2 file(s) | 78 | 2 | killed |
| `r1965.R12_stays_ignores_leaving` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 7 | killed |
| `r1965.R13_stays_ignores_others` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 4 | killed |
| `r1965.R14_settled_not_left` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 2 | killed |
| `r1965.R15_alongside_alone_asks_nothing` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 4 | killed |
| `r1965.R16_unnamed_alongside_moved` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 1 | killed |
| `r1965.R17_alongside_not_removed` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 10 | killed |
| `r1965.R18_asked_by_band_only` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 3 | killed |
| `r1965.R24_sample_second_entry` | `src/cratekit/adopt/move.py` | user | 9 file(s) | 432 | 1 | killed |
| `u339.M21_cross_add` | `src/cratekit/adopt/move.py` | user | 5 file(s) | 245 | 2 | killed |
| `u340.R14_elsewhere_asked` | `src/cratekit/adopt/move.py` | user | 2 file(s) | 143 | 1 | killed |
| `u340.R27_move_split_kept` | `src/cratekit/adopt/move.py` | user | 4 file(s) | 816 | 6 | killed |
| `r1965.R19_worker_leavable` | `src/cratekit/adopt/move_cli.py` | user | 9 file(s) | 432 | 8 | killed |
| `r1965.R20_done_ignores_alongside` | `src/cratekit/adopt/move_cli.py` | user | 9 file(s) | 432 | 1 | killed |
| `r1965.R21_read_back_bands_only` | `src/cratekit/adopt/move_cli.py` | user | 9 file(s) | 432 | 1 | killed |
| `r1965.R22_read_back_everything` | `src/cratekit/adopt/move_cli.py` | user | 9 file(s) | 432 | 1 | killed |
| `r1965.R23_discharge_per_track` | `src/cratekit/adopt/move_cli.py` | user | 9 file(s) | 432 | 1 | killed |
| `u339-composites.M24_discharge_moved` | `src/cratekit/adopt/move_cli.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `u339.M23_worker_into` | `src/cratekit/adopt/move_cli.py` | user | 5 file(s) | 245 | 1 | killed |
| `u340.R16_worker_last_entry` | `src/cratekit/adopt/move_cli.py` | user | 2 file(s) | 143 | 3 | killed |
| `r1965.R07_folders_every_place` | `src/cratekit/adopt/placements.py` | user | 9 file(s) | 432 | 1 | killed |
| `r1965.R09_alongside_not_known` | `src/cratekit/adopt/placements.py` | user | 9 file(s) | 432 | 9 | killed |
| `r1965.R10_others_never_read` | `src/cratekit/adopt/placements.py` | user | 9 file(s) | 432 | 5 | killed |
| `r1950.A02_second_entry_without_place` | `src/cratekit/adopt/plan.py` | user | 3 file(s) | 125 | 1 | killed |
| `r1950.A05_second_beside_without_first_place` | `src/cratekit/adopt/plan.py` | user | 3 file(s) | 125 | 1 | killed |
| `r1965.R01_manual_class_beside` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 7 | killed |
| `r1965.R03_genre_sub_beside` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 2 | killed |
| `r1965.R04_no_mirrored_class` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 5 | killed |
| `r1965.R05_own_folder_always` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 2 | killed |
| `r1965.R06_own_folder_former` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 1 | killed |
| `u340.R10_plan_no_second_entry` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 816 | 10 | killed |
| `u340.R26_apply_split_kept` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 816 | 2 | killed |
| `u23-round-8-independent-composites.X6_adoptable_widens_to_online_only__rerun` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 619 | 5 | killed |
| `u339-composites.C6_census_tombstone` | `src/cratekit/adopt/scan.py` | user | 7 file(s) | 1018 | 49 | killed |
| `u340.R08_census_no_second` | `src/cratekit/adopt/scan.py` | user | 3 file(s) | 758 | 1 | killed |
| `u340.R09_census_unread_raises` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 671 | 32 | killed |
| `u306.A2_zero_state` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 213 | 4 | killed |
| `u306.A3_walk_recursive` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 213 | 18 | killed |
| `u342.P11_restore_keeps_a_stamp` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 2 | killed |
| `u342.P3_headless_is_stamped` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 12 | killed |
| `u342.P4_stamped_apart` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 10 | killed |
| `u342.P5_stamped_writes` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 8 | killed |
| `u342.P9_stamped_key_tag` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 3 | killed |
| `u343.M08_resume_reads_the_name_alone` | `src/cratekit/analysis/run.py` | user | 4 file(s) | 503 | 7 | killed |
| `u343.M09_resume_reads_the_mark_alone` | `src/cratekit/analysis/run.py` | user | 4 file(s) | 503 | 10 | killed |
| `u343.M10_mark_reads_the_wrong_field` | `src/cratekit/analysis/run.py` | user | 3 file(s) | 231 | 6 | killed |
| `u171.Z3_floor_lowered` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 27 | 2 | killed |
| `u171.Z5_floor_raised` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 27 | 2 | killed |
| `u171.Z7_any_for_mean` | `src/cratekit/analysis/vocal.py` | user | 2 file(s) | 27 | 6 | killed |
| `r395.M10_vocals_literal` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 1 | killed |
| `u171.Z1_round_to_ceil` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 27 | 3 | killed |
| `u171.Z2_round_to_truncate` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 27 | 2 | killed |
| `u171.Z8_silence_is_undecodable` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 27 | 1 | killed |
| `u181.V1_unavailable_ignores_bound_loader` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 524 | 5 | killed |
| `u181.V2_torch_failure_kind` | `src/cratekit/analysis/vocals.py` | user | 2 file(s) | 453 | 1 | killed |
| `u92-author.G1_guard_deleted` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 4 | killed |
| `u92-author.G9_warning_counts_the_wrong_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 5 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7231 | 47 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7231 | 22 | killed |
| `u168.C10_argv_never` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1028 | 5 | killed |
| `u168.C11_argv_whole_line` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1028 | 3 | killed |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 9 file(s) | 1131 | 3 | killed |
| `u211.D1_refusal_keeps_its_run` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1200 | 2 | killed |
| `u211.D2_continue_step_named` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1200 | 2 | killed |
| `u248.L4_listing_drops_the_stub_line` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1235 | 4 | killed |
| `u274.I1_context_drops_warnings` | `src/cratekit/cli/__init__.py` | user | 6 file(s) | 450 | 3 | killed |
| `r1991.V1_matching_over_unread` | `src/cratekit/cli/converge.py` | user | 4 file(s) | 387 | 1 | killed |
| `r1991.V2_unread_last` | `src/cratekit/cli/converge.py` | user | 4 file(s) | 387 | 3 | killed |
| `r1991.V3_count_dropped` | `src/cratekit/cli/converge.py` | user | 4 file(s) | 387 | 1 | killed |
| `r2020.M24_converge_no_advice` | `src/cratekit/cli/converge.py` | user | 4 file(s) | 261 | 2 | killed |
| `r239-b.S5_converge_key_off` | `src/cratekit/cli/converge.py` | user | 7 file(s) | 724 | 2 | killed |
| `u89.C1_converge_threshold` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 197 | 2 | killed |
| `u170.D1_kept_folded` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.D2_status_week` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.D3_open_runs_short` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.D4_line_dropped` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1739 | 3 | killed |
| `u211.C1_doctor_closed_is_a_note` | `src/cratekit/cli/doctor_library.py` | user | 2 file(s) | 463 | 1 | killed |
| `u211.C2_doctor_paths_take_no_copy` | `src/cratekit/cli/doctor_library.py` | user | 3 file(s) | 514 | 1 | killed |
| `r745-b.C1_pending_name_accepted` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-b.C3_create_not_exclusive` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 2 | killed |
| `r745-b.C4_torn_file_left` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-b.C5_made_folders_left` | `src/cratekit/cli/export_collection.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r745-b.C6_folder_not_asked_before_the_copy` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-b.C8_live_database_opened` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r745-c.C2_existing_file_not_checked_first` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r745-c.C7_a_file_taken_for_a_folder` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-b.C10_summary_remapped_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-b.C1_no_rule_handed_to_the_emitter` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r773-b.C2_root_not_the_library_root` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-b.C3_warning_not_given` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-b.C4_warning_counts_prefixes_as_rows` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 5 | killed |
| `r773-b.C5_prefix_cap_two` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r773-b.C6_rest_of_the_prefixes_not_counted` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 2 | killed |
| `r773-b.C7_check_always_ok` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r773-b.C8_summary_unmapped_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 3 | killed |
| `r773-b.C9_summary_left_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 94 | 1 | killed |
| `r1349.E2_open_left` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 10 | killed |
| `r1349.E3_offer_unrecorded` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 47 | killed |
| `r1349.N4_open_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 15 | killed |
| `u168.C12_argv_not_saved` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 1035 | 5 | killed |
| `u170.G2_idle_from_start_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1739 | 3 | killed |
| `u170.G3_idle_from_write_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.G4_unstattable_is_old` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.G5_no_abort_retired` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1739 | 2 | killed |
| `u170.G6_missing_verb_branch` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.G8_malformed_stamp` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u183.M16_record_written_only_when_set` | `src/cratekit/cli/gates.py` | maintainer | 4 file(s) | 127 | 2 | killed |
| `u183.M17_record_read_back` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 86 | 7 | killed |
| `u183.M18_load_refuses_non_object` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 112 | 1 | killed |
| `u49-author.G1_an_explicit_gate_takes_an_inline_answer_again` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 37 | 1 | killed |
| `u274.H1_drive_not_entered` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 450 | 17 | killed |
| `u274.H2_warnings_dropped` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 450 | 3 | killed |
| `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 345 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 345 | 21 | killed |
| `u182.M13_identity_parse` | `src/cratekit/cli/jobs.py` | user | 2 file(s) | 155 | 3 | killed |
| `r1499.L01_go_arrival_after_tail` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.L02_go_kept_after_arrival` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 325 | 3 | killed |
| `u190.L10_rest_of_tail_after_a_step_gate` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 1 | killed |
| `u190.L11_done_keeps_the_go_outcome` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 1 | killed |
| `u190.L1_no_tail_returns_untouched` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 146 | killed |
| `u190.L2_land_of_needs_a_mapping` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 56 | killed |
| `u190.L3_landing_carries_manifest` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 19 | killed |
| `u190.L4_landing_carries_pass` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 19 | killed |
| `u190.L5_land_stop_rekordbox_visit` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 1 | killed |
| `u190.L6_way_on_from_the_stopped_step` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 1 | killed |
| `u190.L7_pending_id_names_the_go` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 1 | killed |
| `u190.L9_verify_verb_by_step` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1225 | 1 | killed |
| `u239.L01_remember_land_only` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 1 | killed |

## Zero rows and what they owe

- `u339-composites.M24_discharge_moved` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u23-round-8-independent-composites.X6_adoptable_widens_to_online_only__rerun` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u251.W1_drop_worksteal`

pyproject addopts: drop --dist worksteal, so the suite runs under xdist's default distribution again

- File: `pyproject.toml`
- Source: `u251.json`, row `W1_drop_worksteal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_suite_distribution.py`, `tests/test_mutation_driver.py`, `tests/test_cloud_battery.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_suite_distribution.py::test_a_run_whose_tests_moved_reports_every_test_once`
  - `tests/test_suite_distribution.py::test_the_mutation_driver_passes_the_distribution_on`
  - `tests/test_suite_distribution.py::test_the_suite_runs_on_every_core_and_steals_queued_work`

Old text:

```
addopts = "-q -n auto --dist worksteal"
```

New text:

```
addopts = "-q -n auto"
```

### `u251.W2_dist_load`

pyproject addopts: name --dist load in its place, the default written out

- File: `pyproject.toml`
- Source: `u251.json`, row `W2_dist_load`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_suite_distribution.py`, `tests/test_mutation_driver.py`, `tests/test_cloud_battery.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_suite_distribution.py::test_the_mutation_driver_passes_the_distribution_on`
  - `tests/test_suite_distribution.py::test_the_suite_runs_on_every_core_and_steals_queued_work`

Old text:

```
addopts = "-q -n auto --dist worksteal"
```

New text:

```
addopts = "-q -n auto --dist load"
```

### `u251.W3_driver_strips_the_distribution`

mutate.pytest_addopts: strip --dist and worksteal as well as -q, so the driver's children run under the default distribution

- File: `scripts/mutate.py`
- Source: `u251.json`, row `W3_driver_strips_the_distribution`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_suite_distribution.py`, `tests/test_mutation_driver.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_mutation_driver.py::test_the_count_and_the_failure_survive_a_steal`
  - `tests/test_suite_distribution.py::test_the_mutation_driver_passes_the_distribution_on`

Old text:

```
    return " ".join(token for token in tokens if token not in {"-q", "-qq", "--quiet"})
```

New text:

```
    return " ".join(
        token for token in tokens if token not in {"-q", "-qq", "--quiet", "--dist", "worksteal"}
    )
```

### `u197.M7_display_name`

__name_display__: pin the state directory back to the upstream name

- File: `src/cratekit/_vendor/downloader/__init__.py`
- Source: `u197.json`, row `M7_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 44 against a baseline of 44
- Kills: 7 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_a_file_under_the_old_name_is_not_moved_into_the_state_directory_slot`
  - `tests/test_vendor_import.py::test_a_move_lost_to_another_process_resolves_the_new_directory`
  - `tests/test_vendor_import.py::test_no_old_state_directory_resolves_the_new_one_and_makes_nothing`
  - `tests/test_vendor_import.py::test_the_new_state_directory_wins_and_the_old_one_is_left_alone`
  - `tests/test_vendor_import.py::test_the_old_state_directory_is_moved_into_place_with_its_token`
  - `tests/test_vendor_import.py::test_the_state_directory_name_is_pinned`
  - `tests/test_vendor_import.py::test_the_tree_carries_the_adoption_patch_the_script_declares`

Old text:

```
__name_display__ = "cratekit-downloader"
```

New text:

```
__name_display__ = "tidal-dl-ng"
```

### `u197.M10_adoption_copies`

path_config_base: make an empty new directory instead of moving the old one, leaving the token behind

- File: `src/cratekit/_vendor/downloader/helper/path.py`
- Source: `u197.json`, row `M10_adoption_copies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_a_failed_move_keeps_the_old_state_directory_in_use`
  - `tests/test_vendor_import.py::test_the_old_state_directory_is_moved_into_place_with_its_token`
  - `tests/test_vendor_import.py::test_the_tree_carries_the_adoption_patch_the_script_declares`

Old text:

```
            os.rename(path_before, path_base)
```

New text:

```
            os.makedirs(path_base)
```

### `u197.M11_failed_move_fallback`

path_config_base: a failed move resolves the new, empty directory instead of the old one holding the token

- File: `src/cratekit/_vendor/downloader/helper/path.py`
- Source: `u197.json`, row `M11_failed_move_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_a_failed_move_keeps_the_old_state_directory_in_use`
  - `tests/test_vendor_import.py::test_the_tree_carries_the_adoption_patch_the_script_declares`

Old text:

```
            if not os.path.isdir(path_base):
                return path_before
```

New text:

```
            pass
```

### `u197.M12_lost_race_fallback`

path_config_base: a move lost to another process resolves the old directory, which no longer exists

- File: `src/cratekit/_vendor/downloader/helper/path.py`
- Source: `u197.json`, row `M12_lost_race_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_a_move_lost_to_another_process_resolves_the_new_directory`
  - `tests/test_vendor_import.py::test_the_tree_carries_the_adoption_patch_the_script_declares`

Old text:

```
            if not os.path.isdir(path_base):
                return path_before
```

New text:

```
            return path_before
```

### `u197.M13_adopt_only_a_directory`

path_config_base: adopt whatever sits under the old name, a regular file included

- File: `src/cratekit/_vendor/downloader/helper/path.py`
- Source: `u197.json`, row `M13_adopt_only_a_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_a_file_under_the_old_name_is_not_moved_into_the_state_directory_slot`
  - `tests/test_vendor_import.py::test_the_tree_carries_the_adoption_patch_the_script_declares`

Old text:

```
    if not os.path.lexists(path_base) and os.path.isdir(path_before):
```

New text:

```
    if not os.path.lexists(path_base) and os.path.exists(path_before):
```

### `u197.M8_adoption_off`

path_config_base: never adopt the old state directory, so a token written before the rename is stranded

- File: `src/cratekit/_vendor/downloader/helper/path.py`
- Source: `u197.json`, row `M8_adoption_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendor_import.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendor_import.py::test_a_failed_move_keeps_the_old_state_directory_in_use`
  - `tests/test_vendor_import.py::test_the_old_state_directory_is_moved_into_place_with_its_token`
  - `tests/test_vendor_import.py::test_the_tree_carries_the_adoption_patch_the_script_declares`

Old text:

```
    if not os.path.lexists(path_base) and os.path.isdir(path_before):
```

New text:

```
    if False:
```

### `r1115.M1_failed_needs_a_failure`

read_download: drop the rule that a FAILED job settles only with a failed track, so a FAILED job holding none reads as settled

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M1_failed_needs_a_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`

Old text:

```
        and bool(failed)

```

New text:

```
        and True

```

### `r1115.M2_every_failure_for_good`

read_download: drop the rule that every failed track is refused for good, so a transient failure settles and the go lands over it

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M2_every_failure_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-recording-no-cause]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        and len(for_good) == len(failed)

```

New text:

```
        and len(for_good) >= 0

```

### `r1115.M3_nothing_left_to_run`

read_download: drop the rule that no track is still to run, so a FAILED job with a track never attempted settles

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M3_nothing_left_to_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-track-never-attempted]`

Old text:

```
        and all(item.state in finished for item in held)

```

New text:

```
        and any(item.state in finished for item in held)

```

### `r1115.M4_retryable_is_not_for_good`

read_download: read every failure with a cause as refused for good, retryable or not

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M4_retryable_is_not_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        item.item_id for item in failed if item.cause is not None and not item.cause.retryable

```

New text:

```
        item.item_id for item in failed if item.cause is not None

```

### `r1115.M5_declined_is_refused`

read_download: leave a declined track out of the refused rows, so a lossy only track is named nowhere on the go's check

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M5_declined_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
        and (item.item_id in for_good or item.state is jobs.ItemState.SKIPPED)

```

New text:

```
        and (item.item_id in for_good)

```

### `r1115.M6_landed_needs_a_track`

DownloadRead.landed: read a settled download with no track done as landed, so a tail is set over an empty folder

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M6_landed_needs_a_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
        return self.settled and self.done > 0

```

New text:

```
        return self.settled

```

### `r1115.M7_done_counts_done`

read_download: count a skipped track as done too

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M7_done_counts_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
        done=sum(1 for item in held if item.state is jobs.ItemState.DONE),

```

New text:

```
        done=sum(1 for item in held if item.state in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)),

```

### `r1115.M8_failed_names_the_failures`

read_download: name no failed track, so the go's own warning for one is never raised

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M8_failed_names_the_failures`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 369 against a baseline of 369
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
        failed=tuple(item.item_id for item in failed if item.item_id in for_good),

```

New text:

```
        failed=(),

```

### `u108-c.G25_drive_maps_ending`

acquire_cli.drive_queued: a parked or half failed job is returned as if it ended clean

- File: `src/cratekit/acquire/cli.py`
- Source: `u108-c.json`, row `G25_drive_maps_ending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_label_sync_go.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 476 against a baseline of 476
- Kills: 31 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - ... and 16 more, see the JSON sidecar

Old text:

```
    jobs.raise_for_state(job)
    return job, warnings
```

New text:

```
    return job, warnings
```

### `u169.A2_any_permanent_declined`

refused_for_good: drop the policy class, so any permanent failure (output-exists) is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A2_any_permanent_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 7 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return not cause.retryable
```

### `u169.A3_worker_never_declines`

handle: re-raise a policy refusal instead of declining it, the base's behaviour

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A3_worker_never_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 9 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
            raise jobs.Declined(exc.cause) from exc
```

New text:

```
            raise
```

### `u169.A4_no_declined_warning`

drive_queued: add no warning for the skipped tracks

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A4_no_declined_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
    warnings = (*warnings, *declined_warnings(store, job))
```

New text:

```
    warnings = tuple(warnings)
```

### `u274.C1_worker_names_no_drive`

acquire.cli: the download worker names no per drive holder, so a download logs in once a track

- File: `src/cratekit/acquire/cli.py`
- Source: `u274.json`, row `C1_worker_names_no_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 17 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_download_worker_names_the_vendored_drive`
  - ... and 2 more, see the JSON sidecar

Old text:

```
handle.per_drive = vendored.drive  # type: ignore[attr-defined]

```

New text:

```
(empty)
```

### `u206-b.M2b_disabled_recall_composite`

Composite: drop recall's days 0 guard AND give every entry at least a day's life, so answers kept before the cache was turned off still answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M2b_disabled_recall_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_answers_kept_before_the_cache_was_turned_off_answer_nothing`
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`

Old text:

```
        global _PROCESS_HITS
        if not self.enabled:
            return None
```

New text:

```
        global _PROCESS_HITS
        self.days = max(self.days, 1)
```

### `u206.M13_write_without_merge`

Cache.remember: write only this entry, dropping what another process wrote since

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M13_write_without_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
            merged = {
                name: entry for name, entry in entries.items() if self._fresh(entry, now) is not None
            }
```

New text:

```
            merged = {}
```

### `u206.M1_recall_never_hits`

Cache.recall: never answer from the file, so every lookup asks the provider again

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M1_recall_never_hits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[streamable]`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[withdrawn]`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        held = self._fresh(entries.get(key), self.clock())
```

New text:

```
        held = None
```

### `u77-c.C1_manifest_version`

manifest_rows: refuse only a version below this build's, so a manifest of a later version is read on the hope its keys still mean what they meant

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C1_manifest_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves[{"manifest": 2, "rows": {}}-version 2]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 2, "rows": {}}-version 2]`

Old text:

```
if isinstance(version, bool) or version != MANIFEST_VERSION:
```

New text:

```
if isinstance(version, bool) or version < MANIFEST_VERSION:
```

### `u77-c.C3_not_a_manifest`

manifest_rows: stop asking whether the document names a manifest version at all, so a list document passed by mistake is not refused by name

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C3_not_a_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_that_is_not_one_is_refused[the list]`
  - `tests/test_landing_labels.py::test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`

Old text:

```
if not isinstance(body, Mapping) or "manifest" not in body:
```

New text:

```
if not isinstance(body, Mapping):
```

### `r1360.J3_prefix_always_lags`

judge_window: a first part beside a window short of the count lags too

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J3_prefix_always_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged4-unpaged4-4-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged5-unpaged5-4-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged9-unpaged9-None-agrees]`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
        return WINDOW_LAGS if counted and len(paged) >= declared else WINDOW_AGREES
```

New text:

```
        return WINDOW_LAGS
```

### `r1360.J4_prefix_uncounted_lags`

judge_window: a first part beside a playlist declaring no count lags

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J4_prefix_uncounted_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged9-unpaged9-None-agrees]`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
WINDOW_LAGS if counted and len(paged) >= declared else
```

New text:

```
WINDOW_LAGS if not counted or len(paged) >= declared else
```

### `r1360.W11_offset_dropped`

playlist_tracks_unpaged: a later request is asked with no offset

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W11_offset_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 19 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
                return playlist.tracks(offset=offset) if offset else playlist.tracks()
```

New text:

```
                return playlist.tracks()
```

### `r1360.W13_declared_unread`

playlist_tracks_unpaged: the walk reads no declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W13_declared_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 24 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_page_carrying_another_version_tag_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_empty_later_page_ends_the_walk`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    declared = getattr(playlist, "num_tracks", None)
    if not _is_count
```

New text:

```
    declared = None
    if not _is_count
```

### `r1360.W1_no_walk`

playlist_tracks_unpaged: a first page short of the declared count is not walked past, as U226 left it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W1_no_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 24 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_page_carrying_another_version_tag_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_empty_later_page_ends_the_walk`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    if not _is_count(declared) or len(rows) >= declared or len(rows) < 2:
        return rows
```

New text:

```
    if True:
        return rows
```

### `r1360.W2_walk_no_overlap`

playlist_tracks_unpaged: each later request starts where the last ended, not one track back

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W2_walk_no_overlap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 19 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        offset = len(rows) - 1

```

New text:

```
        offset = len(rows)

```

### `r1360.W7_full_page_ends`

playlist_tracks_unpaged: a full later page ends the walk as a short one does

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W7_full_page_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[250-3]`

Old text:

```
        if len(page) < step:
            break
```

New text:

```
        if len(page) <= step:
            break
```

### `r1360.W8_overlap_kept`

playlist_tracks_unpaged: the overlapping track is read twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W8_overlap_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
- Kills: 25 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        rows.extend(page[1:])
```

New text:

```
        rows.extend(page)
```

### `u226.M1_equal_not_agreed`

judge_window: two equal reads are not read as agreeing first

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M1_equal_not_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 785 against a baseline of 785
- Kills: 78 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_outbound_window_lag.py::test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged0-unpaged0-2-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged1-unpaged1-3-agrees]`
  - `tests/test_prune.py::test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent`
  - `tests/test_prune.py::test_a_settled_track_the_listing_hides_is_not_recorded_as_off`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - ... and 63 more, see the JSON sidecar

Old text:

```
    if unpaged == paged:
        return WINDOW_AGREES
```

New text:

```
    if False:
        return WINDOW_AGREES
```

### `u226.M4_prefix_as_subset`

judge_window: any unpaged read whose tracks the window holds agrees, wherever they stand

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M4_prefix_as_subset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 785 against a baseline of 785
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
paged[: len(unpaged)] == unpaged
```

New text:

```
set(unpaged) <= set(paged)
```

### `u252.L1_ladder_exponent`

fetch_with_retry: double every wait, 2, 4, 8, 16 and 16 in place of 1, 2, 4, 8 and 16

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L1_ladder_exponent`
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
            sleep(min(max_delay, base_delay * (2 ** (attempt - 1))))
```

New text:

```
            sleep(min(max_delay, base_delay * (2 ** attempt)))
```

### `u252.L2_ladder_rungs`

DEFAULT_MAX_RETRIES: four rungs in place of five, so a reading waits 15 seconds and asks four times

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L2_ladder_rungs`
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
DEFAULT_MAX_RETRIES = 5
```

New text:

```
DEFAULT_MAX_RETRIES = 4
```

### `u252.L3_ladder_ceiling_off_by_one`

fetch_with_retry: re-raise at the ceiling one attempt early

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L3_ladder_ceiling_off_by_one`
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
            if attempt > max_retries:
```

New text:

```
            if attempt >= max_retries:
```

### `u252.L4_ladder_cap`

DEFAULT_MAX_DELAY_S: cap a wait at 8 seconds in place of 30, so the last rung waits 8 not 16

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L4_ladder_cap`
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
DEFAULT_MAX_DELAY_S = 30.0
```

New text:

```
DEFAULT_MAX_DELAY_S = 8.0
```

### `u252.L5_ladder_base`

DEFAULT_BASE_DELAY_S: halve the first wait, the coefficient of every rung

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L5_ladder_base`
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
DEFAULT_BASE_DELAY_S = 1.0
```

New text:

```
DEFAULT_BASE_DELAY_S = 0.5
```

### `u252.L6_no_ladder`

fetch_with_retry: take every failure as not retryable, so a timeout is re-raised at the first attempt with no wait

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L6_no_ladder`
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
            if isinstance(exc, CratekitError) and not exc.cause.retryable:
```

New text:

```
            if True:
```

### `u265.M4_query_not_sorted`

_approximate: score the wanted token unsorted against the sorted library names

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M4_query_not_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 42 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbor Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Light]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Lighte]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        _sorted_words(wanted.recording),
        sorted_choices,
```

New text:

```
        wanted.recording,
        sorted_choices,
```

### `u265.M5_hit_named_by_its_sorted_form`

_approximate: look a hit up by its sorted string rather than its position, so any recording whose words were not already in order loses its files

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M5_hit_named_by_its_sorted_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 61 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - ... and 46 more, see the JSON sidecar

Old text:

```
        held for _sorted, _score, position in found for held in index.versions(recordings[position])
```

New text:

```
        held for _sorted, _score, position in found for held in index.versions(_sorted)
```

### `u305.M4_index_library_not_reexported`

match: stop re-exporting index_library, so every caller of match.index_library and the intake suite's patch of it lose their target

- File: `src/cratekit/acquire/match.py`
- Source: `u305.json`, row `M4_index_library_not_reexported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`, `tests/intake/test_workers.py`
- Collected: 709 against a baseline of 709
- Kills: 301 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_answers_that_could_not_be_kept_are_said_on_both_verbs`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_reports_the_coverage_rule_and_a_gap_is_paid_for_again_and_nothing_else_is`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - ... and 286 more, see the JSON sidecar

Old text:

```
    index_library,

```

New text:

```
(empty)
```

### `u305.M1_recorded_recording_swapped`

Recorded.recording: fold the title as the artist and the artist as the title, so a list row and a held file disagree on their recording

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u305.json`, row `M1_recorded_recording_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`
- Collected: 642 against a baseline of 642
- Kills: 71 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index`
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`
  - `tests/test_match_states.py::test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none`
  - `tests/test_match_states.py::test_a_head_inside_the_title_tag_is_stripped_so_a_plain_provider_row_matches`
  - `tests/test_match_states.py::test_a_head_only_in_the_filename_with_a_plain_tag_indexes_as_it_did`
  - `tests/test_match_states.py::test_a_head_written_as_a_suffix_inside_the_tag_comes_off_as_it_does_from_the_stem`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template`
  - `tests/test_match_states.py::test_a_headless_file_takes_its_key_from_initialkey_and_has_none_without_it`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_plain_title_tag_is_untouched_by_the_head_strip`
  - `tests/test_match_states.py::test_a_present_artist_tag_is_never_thrown_away_by_the_pair_fallback`
  - ... and 56 more, see the JSON sidecar

Old text:

```
        return recording_token(self.artist, self.title)
```

New text:

```
        return recording_token(self.title, self.artist)
```

### `u249.M01_path_alone`

_read_from_disk: answer any remembered path whatever its stamp, the path alone as identity

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M01_path_alone`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 7 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and True

```

### `u249.M02_size_out_of_stamp`

_read_from_disk: compare the stamp without its size

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M02_size_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[1:] == stamp[1:]

```

### `u249.M03_mtime_out_of_stamp`

_read_from_disk: compare the stamp without its modification time

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M03_mtime_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:1] + entry.stamp[2:] == stamp[:1] + stamp[2:]

```

### `u249.M04_ctime_out_of_stamp`

_read_from_disk: compare the stamp without its change time, so a restore tool's old time over new bytes is answered from memory

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M04_ctime_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:2] + entry.stamp[3:] == stamp[:2] + stamp[3:]

```

### `u249.M05_inode_out_of_stamp`

_read_from_disk: compare the stamp without its inode

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M05_inode_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:3] + entry.stamp[4:] == stamp[:3] + stamp[4:]

```

### `u249.M06_device_out_of_stamp`

_read_from_disk: compare the stamp without its device

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M06_device_out_of_stamp`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:4] == stamp[:4]

```

### `u249.M07_size_not_stat`

_stamp_of: stamp a constant in place of the file's size

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M07_size_not_stat`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return (0, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

### `u249.M08_template_out_of_key`

_read_from_disk: key the memory on the path alone, so an entry parsed under one name template answers another

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M08_template_out_of_key`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_name_template_is_part_of_the_key`

Old text:

```
    key = (path, template)
```

New text:

```
    key = (path, None)
```

### `u249.M09_no_window`

_read_from_disk: answer an equal stamp from memory however recent the file's modification time

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M09_no_window`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 4 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_to_the_same_size_inside_the_window_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and True

```

### `u249.M10_window_halved`

REMEMBER_WINDOW_NS: one second in place of two, under a FAT volume's step

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M10_window_halved`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
REMEMBER_WINDOW_NS = 2_000_000_000
```

New text:

```
REMEMBER_WINDOW_NS = 1_000_000_000
```

### `u249.M11_window_boundary`

_read_from_disk: a file exactly two seconds older than its entry is read again rather than answered

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M11_window_boundary`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and stamp[1] < entry.made_ns - REMEMBER_WINDOW_NS

```

### `u249.M12_moment_after_read`

_read_from_disk: take the entry's moment after the read, so a write during the read can be answered from memory

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M12_moment_after_read`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`

Old text:

```
    owned, whole = _read_fresh(path, template)
    if stamp is not None and whole:
```

New text:

```
    owned, whole = _read_fresh(path, template)
    made_ns = _now_ns()
    if stamp is not None and whole:
```

### `u249.M13_failed_read_remembered`

_read_from_disk: remember a read that failed, so a moment's I/O error on a USB volume answers every later job

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M13_failed_read_remembered`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`

Old text:

```
    if stamp is not None and whole:
```

New text:

```
    if stamp is not None:
```

### `u249.M14_unstated_remembered_never`

_stamp_of: answer None for every file, so nothing is ever remembered and every walk opens every file

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M14_unstated_remembered_never`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 11 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_pass_of_three_playlists_opens_each_library_file_once`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_removed_file_is_absent_a_new_one_is_read_and_a_renamed_one_is_read_under_its_name`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return None
```

### `u249.M20_reset_forgets_nothing`

match.reset_cache: forget nothing

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M20_reset_forgets_nothing`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_that_cannot_be_stated_is_read_as_before_and_never_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_a_test_starts_with_nothing_remembered`

Old text:

```
    test can clear is a memory that leaks one test's library into the next."""
    _REMEMBERED.clear()
```

New text:

```
    test can clear is a memory that leaks one test's library into the next."""
```

### `u249.M20a_failed_read_keeps_old_entry`

_read_from_disk: keep an earlier whole read's entry when a later read is not whole, so a stamp that comes back brings the old tags back

- File: `src/cratekit/acquire/match_library.py`
- Source: `u249.json`, row `M20a_failed_read_keeps_old_entry`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 780 against a baseline of 780
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
    else:
        # A read that was not whole, or a file with no stamp, forgets what an
        # earlier whole read left: the file has been seen changing, and a stamp
        # that came back later must not bring the older answer back with it.
        _REMEMBERED.pop(key, None)
    return owned
```

New text:

```
    return owned
```

### `u265.M6_cache_misaligned`

sorted_recordings: build the sorted names in reverse, so a position the scorer returns names a different recording

- File: `src/cratekit/acquire/match_library.py`
- Source: `u265.json`, row `M6_cache_misaligned`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 15 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in recordings))
```

New text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in reversed(recordings)))
```

### `u213.M5_listed_names_artist`

listed_names: read no artist off a refused row

- File: `src/cratekit/acquire/match_list.py`
- Source: `u213.json`, row `M5_listed_names_artist`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_match_states.py::test_listed_names_reads_a_row_the_reader_refuses`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)
```

New text:

```
    return str(_field(row, "id", "")).strip(), "", _raw_title(row)
```

### `r1694.S2_tolerance_always`

materialised_session: tolerate a store failure even when no callback was given, so the drive's own catch and streamrip's scope lose their failure

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S2_tolerance_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 209 against a baseline of 209
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_scope_that_asked_for_no_tolerance_still_raises_its_write_back_failure`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if unstored is None:
            write_back(name, path, codec=codec, stored=payload)
        else:

```

New text:

```
        if False:
            write_back(name, path, codec=codec, stored=payload)
        else:
            unstored = unstored or (lambda exc: None)

```

### `r1694.S4_failures_no_credential`

STORE_FAILURES: drop the credential errors, so the keychain's own refusal on the opt in fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S4_failures_no_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 209 against a baseline of 209
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_leaves_a_park_its_own_cause`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    CratekitError,
    OSError,
)
```

### `r1694.S5_failures_no_cratekit`

STORE_FAILURES: drop CratekitError, so an index the write could not read fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S5_failures_no_cratekit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    OSError,
)
```

### `r1694.S6_failures_no_oserror`

STORE_FAILURES: drop OSError, so an index file the write could not make fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S6_failures_no_oserror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    CratekitError,
)
```

### `u274.P1_gone_never`

_gone: read a process that is gone as alive, so a hard killed drive's token directory is never swept

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P1_gone_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`

Old text:

```
    except ProcessLookupError:
        return True

```

New text:

```
    except ProcessLookupError:
        return False

```

### `u274.P4_sweep_live`

sweep_orphans: drop the process check, so every directory of the form is removed, a live drive's token included

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P4_sweep_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 7 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_no_session_file_is_left_anywhere_under_the_state_roots[vendored]`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[catalogue]`
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_a_directory_whose_process_it_cannot_see`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_alone_what_it_cannot_prove_is_an_orphan[own-process]`

Old text:

```
        if owned is None or not _gone(int(owned.group(1))):

```

New text:

```
        if owned is None:

```

### `u274.P5_sweep_not_dir`

sweep_orphans: drop the directory check, so a file or a link of the name is reported removed

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P5_sweep_not_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_the_sweep_reports_only_what_it_removed[file]`
  - `tests/test_vendored_drive.py::test_the_sweep_reports_only_what_it_removed[symlink]`

Old text:

```
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:

```

New text:

```
        if info.st_uid != account:

```

### `u274.P6_sweep_other_account`

sweep_orphans: drop the owner check, so another account's directory is removed

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P6_sweep_other_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_another_accounts_directory_alone`

Old text:

```
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:

```

New text:

```
        if not stat.S_ISDIR(info.st_mode):

```

### `u274.P7_no_sweep`

materialised_session: never sweep, so a hard killed drive's token file stays in the temporary directory

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P7_no_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`

Old text:

```
    sweep_orphans()
    # mkdtemp
```

New text:

```
    # mkdtemp
```

### `u274.P8_captured_always`

captured: take every field the client holds, so a float expiry read back from an int one writes the keychain on every drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P8_captured_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_an_unchanged_session_needs_no_keychain_write_at_all`

Old text:

```
        if value != stored.get(name):
            refreshed[name] = value

```

New text:

```
        refreshed[name] = value

```

### `u274.P9_captured_nothing`

captured: take no field, so a token the provider refreshed during the drive never reaches the keychain

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P9_captured_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 6 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if value != stored.get(name):
            refreshed[name] = value

```

New text:

```
        if False:
            refreshed[name] = value

```

### `r1694.V1_drive_failures_narrowed`

vendored.drive: catch only credential errors at the close, so an index or file failure at a finished drive's close replaces its answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r1694.json`, row `V1_drive_failures_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_provider_session_unstored.py`, `tests/test_acquire_workers.py`
- Collected: 130 against a baseline of 130
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        except provider_session.STORE_FAILURES as exc:
```

New text:

```
        except provider_session.STORE_FAILURES[:1] as exc:
```

### `u274.V11_defect_swallowed`

drive: swallow a defect at the close of a drive that returned

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V11_defect_swallowed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`

Old text:

```
        except Exception:
            if finished:
                raise

```

New text:

```
        except Exception:
            pass

```

### `u274.V12_scope_per_invocation`

VendoredAdapter._session_scope: ignore the drive, so every track materialises and logs in again

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V12_scope_per_invocation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 16 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_tool_is_built_and_pointed_at_one_token_file_for_the_whole_drive`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        held = _DRIVE.get()
        if held is not None:
            return nullcontext(held)

```

New text:

```
(empty)
```

### `u274.V1_refusal_forgotten`

_refuse_if_refused: ask nothing, so a source that met a refusal logs in or asks again

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V1_refusal_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 4 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_fetch_that_meets_a_dead_session_is_remembered`
  - `tests/test_vendored_drive.py::test_a_refusal_outlives_the_source_it_was_met_on`
  - `tests/test_vendored_drive.py::test_a_refused_source_raises_again_with_no_call`
  - `tests/test_vendored_drive.py::test_a_session_refused_mid_track_is_never_asked_again`

Old text:

```
        if self._refused is not None:
            raise AdapterAuthFailed(str(self._refused), remedy=self._refused.remedy)

```

New text:

```
        pass

```

### `u274.V2_login_refusal_unrecorded`

authenticate: do not record a refused login, so a later track of the drive logs in again into the refused session

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V2_login_refusal_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refusal_outlives_the_source_it_was_met_on`
  - `tests/test_vendored_drive.py::test_a_refused_source_raises_again_with_no_call`

Old text:

```
        except AdapterAuthFailed as refused:
            self._refused = refused
            raise

```

New text:

```
        except AdapterAuthFailed as refused:
            raise

```

### `u274.V5_source_per_track`

_Drive.source: never reuse the held source, so every track logs in again (the card's six calls a track)

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V5_source_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 14 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_tool_is_built_and_pointed_at_one_token_file_for_the_whole_drive`
  - `tests/test_vendored_drive.py::test_two_drives_log_in_twice`

Old text:

```
        if held is not None and held.settings.gate == settings.gate:

```

New text:

```
        if False:

```

### `u274.V6_no_rebind`

_Drive.source: reuse the held source without this track's settings, so every track is told the first track's staging directory

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V6_no_rebind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_each_item_still_lands_in_its_own_staging_directory`

Old text:

```
            held.rebind(settings)
            return held

```

New text:

```
            return held

```

### `u274.V8_atmos_stored`

capture: store whatever the tool holds, a session left in its Atmos client included

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V8_atmos_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_session_left_in_the_atmos_client_is_not_stored`

Old text:

```
        if getattr(self._tidal, "is_atmos_session", False):
            return

```

New text:

```
(empty)
```

### `u274.V9_no_capture`

_Drive.close: skip the capture, so a refresh during the drive never reaches the keychain

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V9_no_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 7 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
            if self._scope is not None and self._source is not None:
                self._source.capture(self._scope)

```

New text:

```
            pass

```

### `u254.M07_always_append`

mark_applied: append even to a torn, absent or schema 1 ledger

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M07_always_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 86 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`
  - ... and 71 more, see the JSON sidecar

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if True:
                config.append_durable_bytes(line, path)
```

### `u339.M25_record_union`

record: a second run replaces the folders an entry still waits on

- File: `src/cratekit/adopt/genre_moves.py`
- Source: `u339.json`, row `M25_record_union`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 78 against a baseline of 78
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_genre_given_again_after_the_approval_refuses_the_move_stale`
  - `tests/test_tag_set_move.py::test_a_track_leaving_two_folders_in_one_job_spends_both`

Old text:

```
(kept.get(str(content_id), set()) | set(buckets)) - {into}
```

New text:

```
set(buckets) - {into}
```

### `r1965.R12_stays_ignores_leaving`

alongside_left: count a band being left as keeping the Favorites

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R12_stays_ignores_leaving`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_favorites_another_playlist_keeps_is_not_asked_alone_and_not_left_beside_a_band`
  - `tests/test_tag_set_move.py::test_a_favourite_with_no_vocal_sub_leaves_the_old_favorites`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_place_beside_the_band_still_held_is_read_back_unfinished_and_a_resume_finishes`
  - `tests/test_tag_set_move.py::test_a_row_filed_in_a_genre_sub_leaves_it_with_the_band`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`
  - `tests/test_tag_set_move.py::test_a_vocal_favourite_leaves_the_old_folders_with_vox_and_favorites_too`

Old text:

```
        if in_own_folder(declared, bucket, sub)
    } - set(leaving)
```

New text:

```
        if in_own_folder(declared, bucket, sub)
    }
```

### `r1965.R13_stays_ignores_others`

alongside_left: ignore the folder's other playlists, so Candy no longer keeps Favorites

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R13_stays_ignores_others`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_favorites_another_playlist_keeps_is_not_asked_alone_and_not_left_beside_a_band`
  - `tests/test_tag_set_move.py::test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`
  - `tests/test_tag_set_move.py::test_a_manual_sub_is_never_removed_and_keeps_the_old_folders_favorites`

Old text:

```
    if stays or placements.holds_others(bucket, content_id):
```

New text:

```
    if stays:
```

### `r1965.R14_settled_not_left`

leaving_moved: a band the other bucket settles keeps the Favorites (round one BLOCKING)

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R14_settled_not_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`

Old text:

```
    leaving = (*held, *settled_in_the_other_bucket(entry, bucket, declared))
```

New text:

```
    leaving = held
```

### `r1965.R15_alongside_alone_asks_nothing`

moved_out_of: a track holding only places beside the band is not moved

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R15_alongside_alone_asks_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_derived_class_alone_in_the_old_folder_is_asked_and_left`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_place_beside_the_band_still_held_is_read_back_unfinished_and_a_resume_finishes`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`

Old text:

```
    if not held and not alongside:
        return None
```

New text:

```
    if not held:
        return None
```

### `r1965.R16_unnamed_alongside_moved`

moved_out_of: a place beside the band under another name only does not list the track

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R16_unnamed_alongside_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_derived_class_held_under_another_name_only_is_listed_never_moved`

Old text:

```
                *(set(placements.holds_alongside_unnamed(bucket, entry.content_id)) & set(alongside)),

```

New text:

```
(empty)
```

### `r1965.R17_alongside_not_removed`

moved_out_of: the move removes the bands alone (the R-1965 bug)

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R17_alongside_not_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_derived_class_alone_in_the_old_folder_is_asked_and_left`
  - `tests/test_tag_set_move.py::test_a_derived_class_held_under_another_name_only_is_listed_never_moved`
  - `tests/test_tag_set_move.py::test_a_derived_membership_added_after_the_approval_refuses_the_move_stale`
  - `tests/test_tag_set_move.py::test_a_favorites_another_playlist_keeps_is_not_asked_alone_and_not_left_beside_a_band`
  - `tests/test_tag_set_move.py::test_a_favourite_with_no_vocal_sub_leaves_the_old_favorites`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_place_beside_the_band_still_held_is_read_back_unfinished_and_a_resume_finishes`
  - `tests/test_tag_set_move.py::test_a_row_filed_in_a_genre_sub_leaves_it_with_the_band`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`
  - `tests/test_tag_set_move.py::test_a_vocal_favourite_leaves_the_old_folders_with_vox_and_favorites_too`

Old text:

```
    held = tuple(sorted({*held, *alongside}))
```

New text:

```
    held = tuple(sorted(held))
```

### `r1965.R18_asked_by_band_only`

buckets_asked: ask a moved out bucket only where a band is held

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R18_asked_by_band_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_derived_class_alone_in_the_old_folder_is_asked_and_left`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`

Old text:

```
        if genre_moved_out_of(entry, bucket.id, declared, moved) and any(
            leaving_moved(entry, bucket.id, placements, declared, subs)
        ):
```

New text:

```
        if genre_moved_out_of(entry, bucket.id, declared, moved) and any(
            leaving_moved(entry, bucket.id, placements, declared, subs)[:1]
        ):
```

### `r1965.R24_sample_second_entry`

sample of U339's guard: genre_moved_out_of no longer refuses a second genre's entry

- File: `src/cratekit/adopt/move.py`
- Source: `r1965.json`, row `R24_sample_second_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_track_with_a_second_genre_leaves_only_its_old_folder`

Old text:

```
        and not entry.second

```

New text:

```
(empty)
```

### `u339.M21_cross_add`

moved_out_of: the target is added again though the track already holds it

- File: `src/cratekit/adopt/move.py`
- Source: `u339.json`, row `M21_cross_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_workers.py`
- Collected: 245 against a baseline of 245
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_move_already_half_made_by_adoption_only_removes`
  - `tests/test_tag_set_move.py::test_a_vocal_favourite_leaves_the_old_folders_with_vox_and_favorites_too`

Old text:

```
        add="" if target in placements.holds(into, entry.content_id) else target,
```

New text:

```
        add=target,
```

### `u340.R14_elsewhere_asked`

buckets_asked: ask a bucket the track's other entry claims, so the first entry's tree path plans there too

- File: `src/cratekit/adopt/move.py`
- Source: `u340.json`, row `R14_elsewhere_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adopt_move.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_double_in_the_second_folder_is_moved_once_by_its_own_entry`

Old text:

```
        if bucket.id in elsewhere:
            continue
```

New text:

```
        if bucket.id in elsewhere and False:
            continue
```

### `u340.R27_move_split_kept`

held_in: keep no split place for the other entry, so adopt move takes Soul with R&B out of R&B and the worker reads the band as left (B1, round two)

- File: `src/cratekit/adopt/move.py`
- Source: `u340.json`, row `R27_move_split_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 816 against a baseline of 816
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[rnb]`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[rnb-soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[soul-rnb]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[rnb-soul]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[soul-rnb]`

Old text:

```
    return frozenset(held - kept_beside(declared, bucket, elsewhere))
```

New text:

```
    return frozenset(held)
```

### `r1965.R19_worker_leavable`

remaining: refuse a frozen move naming a place beside the band as no longer competing

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r1965.json`, row `R19_worker_leavable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_derived_membership_added_after_the_approval_refuses_the_move_stale`
  - `tests/test_tag_set_move.py::test_a_favourite_with_no_vocal_sub_leaves_the_old_favorites`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_place_beside_the_band_still_held_is_read_back_unfinished_and_a_resume_finishes`
  - `tests/test_tag_set_move.py::test_a_row_filed_in_a_genre_sub_leaves_it_with_the_band`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`
  - `tests/test_tag_set_move.py::test_a_vocal_favourite_leaves_the_old_folders_with_vox_and_favorites_too`

Old text:

```
            set(plan_engine.alongside_places(declared, move.bucket))
            if move.target_bucket
```

New text:

```
            set()
            if move.target_bucket
```

### `r1965.R20_done_ignores_alongside`

remaining: the cross move done check reads the bands alone, a place beside the band still held read as done

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r1965.json`, row `R20_done_ignores_alongside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`

Old text:

```
            if arrived and not still_to_leave(current.placements, declared, move, held):
```

New text:

```
            if arrived and not held:
```

### `r1965.R21_read_back_bands_only`

still_to_leave: never count a place beside the band, so one left behind reads back moved

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r1965.json`, row `R21_read_back_bands_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_place_beside_the_band_still_held_is_read_back_unfinished_and_a_resume_finishes`

Old text:

```
    return (set(held) | set(beside)) & set(move.remove)
```

New text:

```
    return set(held) & set(move.remove)
```

### `r1965.R22_read_back_everything`

still_to_leave: count everything still held, a band the other bucket settles included (round two row 3)

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r1965.json`, row `R22_read_back_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`

Old text:

```
    return (set(held) | set(beside)) & set(move.remove)
```

New text:

```
    return set(held) | set(beside)
```

### `r1965.R23_discharge_per_track`

handle: spend a genre move whose track has another move unfinished

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r1965.json`, row `R23_discharge_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`

Old text:

```
            if move.content_id not in unfinished:
```

New text:

```
            if True:
```

### `u339-composites.M24_discharge_moved`

handle: an entry is spent though the track was not read back moved

- File: `src/cratekit/adopt/move_cli.py`
- Source: `u339-composites.json`, row `M24_discharge_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_workers.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if move.target_bucket and move.content_id in found["moved"]:
```

New text:

```
        if move.target_bucket:
```

### `u339.M23_worker_into`

remaining: a frozen move whose folder changed is performed

- File: `src/cratekit/adopt/move_cli.py`
- Source: `u339.json`, row `M23_worker_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_workers.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_genre_given_again_after_the_approval_refuses_the_move_stale`

Old text:

```
        if isinstance(now, move_engine.Move) and now.into != move.into:
```

New text:

```
        if False:
```

### `u340.R16_worker_last_entry`

remaining: index entries by track with the last one winning, as before the card

- File: `src/cratekit/adopt/move_cli.py`
- Source: `u340.json`, row `R16_worker_last_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adopt_move.py`
- Collected: 143 against a baseline of 143
- Kills: 3 (killed)
- Killed:
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[rnb-soul]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[soul-rnb]`
  - `tests/test_second_genre.py::test_the_worker_checks_a_move_against_the_entry_that_planned_it`

Old text:

```
    entries = move_engine.entries_by_track(current.entries)
```

New text:

```
    entries = {entry.content_id: (entry,) for entry in current.entries}
```

### `r1965.R07_folders_every_place`

placements_from: take the folder of every competing place, a former place's holder included

- File: `src/cratekit/adopt/placements.py`
- Source: `r1965.json`, row `R07_folders_every_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`

Old text:

```
            if in_own_folder(declared, bucket.id, sub_id):
                folders.update
```

New text:

```
            if True:
                folders.update
```

### `r1965.R09_alongside_not_known`

placements_from: a place beside the band counts among the folder's other playlists

- File: `src/cratekit/adopt/placements.py`
- Source: `r1965.json`, row `R09_alongside_not_known`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 9 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_favourite_with_no_vocal_sub_leaves_the_old_favorites`
  - `tests/test_tag_set_move.py::test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`
  - `tests/test_tag_set_move.py::test_a_genre_move_is_spent_only_when_every_move_of_its_track_finished`
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`
  - `tests/test_tag_set_move.py::test_a_place_beside_the_band_still_held_is_read_back_unfinished_and_a_resume_finishes`
  - `tests/test_tag_set_move.py::test_a_row_filed_in_a_genre_sub_leaves_it_with_the_band`
  - `tests/test_tag_set_move.py::test_a_row_moved_into_the_genre_split_out_of_its_folder_leaves_every_place_there`
  - `tests/test_tag_set_move.py::test_a_vocal_favourite_leaves_the_old_folders_with_vox_and_favorites_too`
  - `tests/test_tag_set_move.py::test_the_reader_files_each_place_beside_the_band_and_the_folders_other_playlists_apart`

Old text:

```
                alongside_unnamed,
            )
            known.update((node.folder_id, node.playlist_id) for node in answering)
```

New text:

```
                alongside_unnamed,
            )
```

### `r1965.R10_others_never_read`

placements_from: never record another playlist of the folder

- File: `src/cratekit/adopt/placements.py`
- Source: `r1965.json`, row `R10_others_never_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`
  - `tests/test_tag_set_move.py::test_a_manual_sub_is_never_removed_and_keeps_the_old_folders_favorites`
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`
  - `tests/test_tag_set_move.py::test_the_reader_files_each_place_beside_the_band_and_the_folders_other_playlists_apart`

Old text:

```
                if (node.folder_id, node.playlist_id) in known:
                    continue
```

New text:

```
                if True:
                    continue
```

### `r1950.A02_second_entry_without_place`

adoption: the second entry is built whenever a routed track names a second bucket, so a second folder with no place for the reading gets an entry that files nothing and keeps a split place for the first; the ledger's sub is None guard, now the caller's if second_sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r1950.json`, row `A02_second_entry_without_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_adopt.py`, `tests/test_second_genre.py`, `tests/test_adopt_split_place.py`
- Collected: 125 against a baseline of 125
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre_guards_adopt.py::test_a_second_folder_with_no_place_for_the_reading_files_nothing_and_keeps_nothing`

Old text:

```
        if second_sub:
            entry = replace(unplaced, genre=track.second_genre, second=True)
```

New text:

```
        if track.second_bucket and track.disposition is Disposition.ROUTE:
            entry = replace(unplaced, genre=track.second_genre, second=True)
```

### `r1950.A05_second_beside_without_first_place`

adoption: the second entry keeps the first bucket's split place even when the first entry files nothing there

- File: `src/cratekit/adopt/plan.py`
- Source: `r1950.json`, row `A05_second_beside_without_first_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_adopt.py`, `tests/test_second_genre.py`, `tests/test_adopt_split_place.py`
- Collected: 125 against a baseline of 125
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre_guards_adopt.py::test_a_second_entry_keeps_no_split_place_beside_a_first_folder_with_no_place`

Old text:

```
                    beside=frozenset({bucket}) if sub else frozenset(),
```

New text:

```
                    beside=frozenset({bucket}),
```

### `r1965.R01_manual_class_beside`

derived_classes: admit a manual class (Candy), so the move removes it

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R01_manual_class_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_no_additive_class_of_the_vocal_identifier_is_no_vocal_sub`
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`
  - `tests/test_tag_set_move.py::test_a_manual_sub_is_never_removed_and_keeps_the_old_folders_favorites`
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`
  - `tests/test_tag_set_move.py::test_the_reader_files_each_place_beside_the_band_and_the_folders_other_playlists_apart`
  - `tests/test_tag_set_move.py::test_the_shipped_places_beside_a_band_are_the_two_derived_classes_and_the_genre_subs`

Old text:

```
        if not entry.additive:
            continue
        others = tuple(other for other in declared.sub_classes if other is not entry)
        # The loader's own list of what a bucket's folder holds, without this class.
        ids, displays = taxonomy.live_places(declared.bucket(bucket_id), declared.energy, others)
        if entry.id not in ids
```

New text:

```
        others = tuple(other for other in declared.sub_classes if other is not entry)
        # The loader's own list of what a bucket's folder holds, without this class.
        ids, displays = taxonomy.live_places(declared.bucket(bucket_id), declared.energy, others)
        if entry.id not in ids
```

### `r1965.R03_genre_sub_beside`

alongside_places: leave the genre subs out, so a Rominimal row keeps its old genre sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R03_genre_sub_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_row_filed_in_a_genre_sub_leaves_it_with_the_band`
  - `tests/test_tag_set_move.py::test_the_shipped_places_beside_a_band_are_the_two_derived_classes_and_the_genre_subs`

Old text:

```
    return (*derived_classes(declared, bucket_id), *genre)
```

New text:

```
    return derived_classes(declared, bucket_id)
```

### `r1965.R04_no_mirrored_class`

mirrored_classes: name no class, so Favorites leaves even while Candy keeps the row in the folder

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R04_no_mirrored_class`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_band_of_another_folder_does_not_keep_this_folders_favorites`
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_favorites_another_playlist_keeps_is_not_asked_alone_and_not_left_beside_a_band`
  - `tests/test_tag_set_move.py::test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`
  - `tests/test_tag_set_move.py::test_a_manual_sub_is_never_removed_and_keeps_the_old_folders_favorites`

Old text:

```
    return frozenset() if found is None else frozenset({found.id})
```

New text:

```
    return frozenset()
```

### `r1965.R05_own_folder_always`

in_own_folder: answer True for every place, a split place of the holder included

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R05_own_folder_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_band_of_another_folder_does_not_keep_this_folders_favorites`
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`

Old text:

```
    if routing.split_place(declared, bucket_id, sub_id) is not None:
        return False
    former
```

New text:

```
    if routing.split_place(declared, bucket_id, sub_id) is not None:
        return True
    former
```

### `r1965.R06_own_folder_former`

in_own_folder: read a former place as the declarer's own folder too

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R06_own_folder_former`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`

Old text:

```
    return former is None or former.bucket == bucket_id
```

New text:

```
    return True
```

### `u340.R10_plan_no_second_entry`

build_adoption_plan: drop the second entry, so adoption never files the second folder

- File: `src/cratekit/adopt/plan.py`
- Source: `u340.json`, row `R10_plan_no_second_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 816 against a baseline of 816
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[rnb]`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[rnb-soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[soul-rnb]`
  - `tests/test_second_genre.py::test_a_track_in_its_second_folder_is_no_stranger_there`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[rnb-soul]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[soul-rnb]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_the_track_in_both_folders`
  - `tests/test_second_genre.py::test_the_plan_gives_a_second_entry_and_counts_the_track_once`
  - `tests/test_second_genre.py::test_the_worker_checks_a_move_against_the_entry_that_planned_it`

Old text:

```
        if second_sub:
            entry = replace(unplaced, genre=track.second_genre, second=True)
```

New text:

```
        if second_sub and False:
            entry = replace(unplaced, genre=track.second_genre, second=True)
```

### `u340.R26_apply_split_kept`

competing_place: drop the split place the other entry keeps no more, so adoption withholds Soul beside R&B (B1)

- File: `src/cratekit/adopt/plan.py`
- Source: `u340.json`, row `R26_apply_split_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 816 against a baseline of 816
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[rnb-soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[soul-rnb]`

Old text:

```
    held = tuple(sorted((set(placements.holds(bucket, content_id)) & competing) - kept))
```

New text:

```
    held = tuple(sorted(set(placements.holds(bucket, content_id)) & competing))
```

### `u23-round-8-independent-composites.X6_adoptable_widens_to_online_only__rerun`

The X6 row again, now that a guard test for it exists. Was zero against the branch as delivered.

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent-composites.json`, row `X6_adoptable_widens_to_online_only__rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
ADOPTABLE: frozenset[Readability] = frozenset({Readability.READABLE})
```

New text:

```
ADOPTABLE: frozenset[Readability] = frozenset(
    {Readability.READABLE, Readability.ONLINE_ONLY}
)
```

### `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed`

What X6 holds: the EXCLUDED disposition itself, forced to ROUTE

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent-composites.json`, row `X6_composite_excluded_becomes_routed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 619 against a baseline of 619
- Kills: 5 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped`
  - `tests/test_adoption.py::test_every_plan_entry_identifier_is_derivable_from_the_record_it_names`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`

Old text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue

```

New text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.ROUTE,
                genre=row.genre,
            )
            continue

```

### `u339-composites.C6_census_tombstone`

scan_rows: a tombstoned row is read as live by the census, the layer M6_tombstone_row's guard sits on (its composite)

- File: `src/cratekit/adopt/scan.py`
- Source: `u339-composites.json`, row `C6_census_tombstone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_behaviour_compare.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`
- Collected: 1018 against a baseline of 1018
- Kills: 49 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`
  - `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
  - `tests/test_tag_backlog.py::test_a_catch_all_is_left_to_tag_retag`
  - `tests/test_tag_backlog.py::test_a_person_reads_the_backlog`
  - `tests/test_tag_backlog.py::test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it`
  - `tests/test_tag_backlog.py::test_a_row_with_no_genre_and_agreeing_neighbours_is_proposed_from_the_neighbours`
  - `tests/test_tag_backlog.py::test_a_row_with_nothing_beside_it_is_left_with_no_votes`
  - `tests/test_tag_backlog.py::test_a_word_neither_answer_takes_leaves_its_rows_with_the_refusal`
  - `tests/test_tag_backlog.py::test_a_word_with_one_answer_moves_only_the_rows_it_reaches`
  - `tests/test_tag_backlog.py::test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`
  - `tests/test_tag_backlog.py::test_only_a_row_with_no_genre_is_asked_of_the_catalogue`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        if row.deleted:
            continue
```

New text:

```
(empty)
```

### `u340.R08_census_no_second`

scan_rows: never name a second bucket, so adoption plans no second entry

- File: `src/cratekit/adopt/scan.py`
- Source: `u340.json`, row `R08_census_no_second`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_the_census_reads_the_second_genre_of_a_routed_track`

Old text:

```
            second_bucket=routing.second_bucket(declared, row.genre, second) or "",
```

New text:

```
            second_bucket="",
```

### `u340.R09_census_unread_raises`

_second_of: let an unreadable file's failure end the census walk

- File: `src/cratekit/adopt/scan.py`
- Source: `u340.json`, row `R09_census_unread_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`
- Collected: 671 against a baseline of 671
- Kills: 32 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_collision_is_addressed_by_the_node_and_survives_a_rename`
  - `tests/test_adoption.py::test_a_container_this_build_cannot_write_costs_one_entry_not_the_run`
  - `tests/test_adoption.py::test_a_declared_folder_that_already_exists_is_surfaced`
  - `tests/test_adoption.py::test_a_failed_write_leaves_the_entry_outstanding`
  - `tests/test_adoption.py::test_a_folder_holding_only_what_the_plan_names_is_not_a_collision`
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one`
  - `tests/test_adoption.py::test_a_recorded_answer_that_is_not_an_approval_applies_nothing`
  - `tests/test_adoption.py::test_a_recorded_location_handed_over_as_a_Path_still_resolves`
  - `tests/test_adoption.py::test_a_row_recorded_THE_WAY_REKORDBOX_RECORDS_ONE_is_adoptable[empty-authority]`
  - `tests/test_adoption.py::test_a_row_recorded_THE_WAY_REKORDBOX_RECORDS_ONE_is_adoptable[localhost]`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_a_second_run_over_a_finished_plan_writes_nothing`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`
  - `tests/test_adoption.py::test_an_approval_for_a_different_plan_is_refused`
  - ... and 17 more, see the JSON sidecar

Old text:

```
        return (reader(path) or "").strip()
    except (tags.TagReadFailed, OSError):
        return ""
```

New text:

```
        return (reader(path) or "").strip()
    except OSError:
        return ""
```

### `u306.A2_zero_state`

analysis.cli.nothing_to_queue: the default state of an empty folder reworded, so the no job payload names another state

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A2_zero_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_with_no_audio_queues_nothing_and_says_so`
  - `tests/test_analysis_workers.py::test_a_restamp_over_an_empty_folder_is_the_honest_zero_whatever_the_calibration`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_vocals_cli.py::test_a_folder_with_no_audio_queues_nothing`

Old text:

```
    ctx, folder: Path, extra: tuple[dict[str, str], ...] = (), *, state: str = "no-audio"
```

New text:

```
    ctx, folder: Path, extra: tuple[dict[str, str], ...] = (), *, state: str = "no-audio-found"
```

### `u306.A3_walk_recursive`

analysis.cli.walk_folder: ignore --recursive, so a nested file is never queued by restamp or vocals

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A3_walk_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
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
```

New text:

```
    recursive = False
```

### `u342.P11_restore_keeps_a_stamp`

apply_adopt: keep only the corrected rows' surfaces in the record, so a restore leaves a stamped file's title tag

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P11_restore_keeps_a_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes]
```

New text:

```
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes if item.action == ADOPT]
```

### `u342.P3_headless_is_stamped`

plan_row: never take the stamp path, so a headless title is left no-head as before U342

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P3_headless_is_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 12 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`
  - `tests/test_analyze_adopt.py::test_a_headless_row_rekordbox_did_not_key_or_time_is_left_and_named`
  - `tests/test_analyze_adopt.py::test_a_headless_row_whose_tag_carries_another_title_is_left`
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_check_names_adopt_for_the_bare_titles_a_landing_since_u343_leaves`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
    if parsed is None:
        # NO HEAD
```

New text:

```
    if False:
        # NO HEAD
```

### `u342.P4_stamped_apart`

plan_row: plan a stamped row as adopt, so the plan does not show it apart

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P4_stamped_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 10 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_check_names_adopt_for_the_bare_titles_a_landing_since_u343_leaves`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
        action = STAMPED

```

New text:

```
        action = ADOPT

```

### `u342.P5_stamped_writes`

WRITING: drop stamped, so a stamped row is planned and never written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P5_stamped_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 8 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_written_message_counts_only_stamped_files_that_took_it`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
WRITING: tuple[str, ...] = (ADOPT, STAMPED)
```

New text:

```
WRITING: tuple[str, ...] = (ADOPT,)
```

### `u342.P9_stamped_key_tag`

plan_row: give only a corrected row rekordbox's key tag, never a stamped one

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P9_stamped_key_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
    if key is not None and parse_camelot(initialkey) != parse_camelot(key):
```

New text:

```
    if action == ADOPT and key is not None and parse_camelot(initialkey) != parse_camelot(key):
```

### `u343.M08_resume_reads_the_name_alone`

already_analyzed: read only the head on the name, so a file marked since U343 is measured again

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M08_resume_reads_the_name_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`, `tests/test_analysis_ahead.py`
- Collected: 503 against a baseline of 503
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_batch_resume_skips_a_file_carrying_the_mark_and_reads_the_rest`
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_reads_the_head_by_the_rule_analyze_run_skips_by`

Old text:

```
    return has_head(path.name, template=template) or marked(path)
```

New text:

```
    return has_head(path.name, template=template)
```

### `u343.M09_resume_reads_the_mark_alone`

already_analyzed: read only the mark, so a file a run before U343 named is measured again

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M09_resume_reads_the_mark_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`, `tests/test_analysis_ahead.py`
- Collected: 503 against a baseline of 503
- Kills: 10 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_killed_batch_resumes_skipping_completed_tracks`
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_vocals_cli.py::test_a_rescore_job_that_does_not_succeed_ends_the_chain_at_the_analyze_step`
  - `tests/test_vocals_cli.py::test_analyze_run_still_skips_a_prefixed_file`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`
  - `tests/test_vocals_cli.py::test_unscored_reads_the_head_by_the_rule_analyze_run_skips_by`

Old text:

```
    return has_head(path.name, template=template) or marked(path)
```

New text:

```
    return marked(path)
```

### `u343.M10_mark_reads_the_wrong_field`

marked: read the drift tag in place of the mark, an identity not unique to the run's measure

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M10_mark_reads_the_wrong_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_batch_resume_skips_a_file_carrying_the_mark_and_reads_the_rest`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_reads_the_head_by_the_rule_analyze_run_skips_by`

Old text:

```
    return tags.read_tag(path, MARK_FIELD) is not None
```

New text:

```
    return tags.read_tag(path, "drift") is not None
```

### `u171.Z3_floor_lowered`

vocal.DEFAULT_FRAME_FLOOR: 0.05 to 0.03, so a lead the model hears at 0.034 scores

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z3_floor_lowered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 27 against a baseline of 27
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

### `u171.Z5_floor_raised`

vocal.DEFAULT_FRAME_FLOOR: 0.05 to 0.10, so a trace heard at 0.08 never counts

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z5_floor_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 27 against a baseline of 27
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

### `u171.Z7_any_for_mean`

vocal.presence_score: any frame at the floor scores 100, so coverage becomes presence

- File: `src/cratekit/analysis/vocal.py`
- Source: `u171.json`, row `Z7_any_for_mean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 27 against a baseline of 27
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

### `r395.M10_vocals_literal`

Put the old bare pip literal back in the vocals install text

- File: `src/cratekit/analysis/vocals.py`
- Source: `r395.json`, row `M10_vocals_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`

Old text:

```
    return extras.install_command("vocals")
```

New text:

```
    return "pip install 'cratekit[vocals]'"
```

### `u171.Z1_round_to_ceil`

vocals.analyse: stamp a trace under half a percent as 1 by rounding the presence up

- File: `src/cratekit/analysis/vocals.py`
- Source: `u171.json`, row `Z1_round_to_ceil`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocal_zeros.py`, `tests/test_analysis.py`
- Collected: 27 against a baseline of 27
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
- Collected: 27 against a baseline of 27
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
- Collected: 27 against a baseline of 27
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

### `u181.V1_unavailable_ignores_bound_loader`

vocals.unavailable: ask missing_requirement even with a loader bound, so a bound fake reads as unable

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V1_unavailable_ignores_bound_loader`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_doctor.py`
- Collected: 524 against a baseline of 524
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

### `u181.V2_torch_failure_kind`

vocals.requirement: a torch that will not import is named as missing files, so doctor offers no reinstall

- File: `src/cratekit/analysis/vocals.py`
- Source: `u181.json`, row `V2_torch_failure_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_doctor.py`
- Collected: 453 against a baseline of 453
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

### `u92-author.G1_guard_deleted`

Delete the oversize guard from analyse entirely, which is main's state

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G1_guard_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
(empty)
```

### `u92-author.G9_warning_counts_the_wrong_reason`

unscored_warning counts size refusals, so an oversize file is reported as a missing model

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G9_warning_counts_the_wrong_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`
  - `tests/test_analysis_workers.py::test_an_oversize_track_is_never_warned_about_as_a_missing_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_MODEL_UNAVAILABLE, 0))
```

New text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_AUDIO_TOO_LARGE, 0))
```

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7231 against a baseline of 7231
- Kills: 47 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - ... and 32 more, see the JSON sidecar

Old text:

```
        parked = isinstance(exc, JobBlocked)
```

New text:

```
        parked = False
```

### `r290-author.D4_cancelled_reads_failed`

Read the cancelled type as the failed outcome, which is what the dispatcher said before Outcome.CANCELLED had a producer

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D4_cancelled_reads_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7231 against a baseline of 7231
- Kills: 22 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            outcome = Outcome.CANCELLED
```

New text:

```
            outcome = Outcome.FAILED
```

### `u168.C10_argv_never`

_dispatched: never record the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C10_argv_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1028 against a baseline of 1028
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_a_continuation_that_refuses_answers_with_its_refusal_and_keeps_the_answer`
  - `tests/test_run_decide_continue.py::test_a_session_answers_and_mints_in_one_command_with_no_actor_given`
  - `tests/test_run_decide_continue.py::test_the_continuation_is_given_the_arguments_its_first_invocation_recorded`

Old text:

```
        if not args.run:
            state.argv = _verb_argv(argv, entry)
```

New text:

```
        if False:
            state.argv = _verb_argv(argv, entry)
```

### `u168.C11_argv_whole_line`

_verb_argv: keep the global options before the verb

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C11_argv_whole_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1028 against a baseline of 1028
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_the_continuation_is_given_the_arguments_its_first_invocation_recorded`

Old text:

```
            return tuple(tokens[index:])
```

New text:

```
            return tuple(tokens)
```

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1131 against a baseline of 1131
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
    if remembered == 0 and asked == 0:
        return envelope
```

New text:

```
    if True:
        return envelope
```

### `u211.D1_refusal_keeps_its_run`

dispatcher: a refusal under the unconfirmed cause is not kept, so the run fails and is not resumable

- File: `src/cratekit/cli/__init__.py`
- Source: `u211.json`, row `D1_refusal_keeps_its_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_cli_contract.py`, `tests/test_job_outcome.py`, `tests/test_run_decide_continue.py`
- Collected: 1200 against a baseline of 1200
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
            isinstance(exc, processes.AbsenceUnconfirmed)
            and cause.reason in gates.KEPT_RUN_REASONS
```

New text:

```
            False
            and cause.reason in gates.KEPT_RUN_REASONS
```

### `u211.D2_continue_step_named`

dispatcher: a kept refusal carries no step naming the command that continues it

- File: `src/cratekit/cli/__init__.py`
- Source: `u211.json`, row `D2_continue_step_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_cli_contract.py`, `tests/test_job_outcome.py`, `tests/test_run_decide_continue.py`
- Collected: 1200 against a baseline of 1200
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        if kept and state is not None:
            cause = _with_run_continue(cause, state)
```

New text:

```
        if False:
            cause = _with_run_continue(cause, state)
```

### `u248.L4_listing_drops_the_stub_line`

ask_for_listing: a missing extra no longer makes the stub, so the listing omits (requires the extra)

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L4_listing_drops_the_stub_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 1235 against a baseline of 1235
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_missing_analysis_extra_names_the_install_command`
  - `tests/test_cli_contract.py::test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command`
  - `tests/test_cli_lazy.py::test_a_blocked_extra_still_lists_the_stub_line_and_refuses_with_the_install_command`
  - `tests/test_vocals_cli.py::test_a_missing_vocals_extra_names_the_install_command`

Old text:

```
            if _is_missing_extra(exc, self.entry):
                self._stub(exc)
```

New text:

```
            if _is_missing_extra(exc, self.entry):
                pass
```

### `u274.I1_context_drops_warnings`

Context.run_job: return the drift warnings only, so the drive's warnings never reach the envelope

- File: `src/cratekit/cli/__init__.py`
- Source: `u274.json`, row `I1_context_drops_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        return result, (*handlers.drift_warnings(result.drifted), *result.warnings)

```

New text:

```
        return result, handlers.drift_warnings(result.drifted)

```

### `r1991.V1_matching_over_unread`

converge: say matching over an unread playlist (the residual at the verb)

- File: `src/cratekit/cli/converge.py`
- Source: `r1991.json`, row `V1_matching_over_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_unrecorded_genre_folder.py`
- Collected: 387 against a baseline of 387
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_never_says_matching_over_an_unrecorded_renamed_folder`

Old text:

```
    if not report.unidentified:
        return MATCHING, detail
```

New text:

```
    if True:
        return MATCHING, detail
```

### `r1991.V2_unread_last`

converge: put the unread playlists after the differences, so the cut at twenty drops them

- File: `src/cratekit/cli/converge.py`
- Source: `r1991.json`, row `V2_unread_last`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_unrecorded_genre_folder.py`
- Collected: 387 against a baseline of 387
- Kills: 3 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_names_a_difference_past_many_unread_playlists`
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_never_says_matching_over_an_unrecorded_renamed_folder`
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_says_differing_over_a_doubled_row_beside_an_unread_folder`

Old text:

```
(*unread[:UNREAD_SHOWN], *report.summaries())[:20]
```

New text:

```
(*report.summaries(), *unread[:UNREAD_SHOWN])[:20]
```

### `r1991.V3_count_dropped`

converge: never say how many playlists were not compared past the five named

- File: `src/cratekit/cli/converge.py`
- Source: `r1991.json`, row `V3_count_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_unrecorded_genre_folder.py`
- Collected: 387 against a baseline of 387
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_names_a_difference_past_many_unread_playlists`

Old text:

```
        if len(unread) > UNREAD_SHOWN:
```

New text:

```
        if False:
```

### `r2020.M24_converge_no_advice`

converge: end a not compared line without the shared wording

- File: `src/cratekit/cli/converge.py`
- Source: `r2020.json`, row `M24_converge_no_advice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_converge_and_the_writes_share_one_wording`
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_never_says_matching_over_an_unrecorded_renamed_folder`

Old text:

```
{'; '.join(unread)}{rebuild.UNIDENTIFIED}"
```

New text:

```
{'; '.join(unread)}"
```

### `r239-b.S5_converge_key_off`

converge passes unlock=False again, so every native tree reads not compared on a real library

- File: `src/cratekit/cli/converge.py`
- Source: `r239-b.json`, row `S5_converge_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`

Old text:

```
            handle = rb_writer.open_db(cfg=cfg)
```

New text:

```
            handle = rb_writer.open_db(cfg=cfg, unlock=False)
```

### `u89.C1_converge_threshold`

converge _compare: pass None instead of the loaded cut

- File: `src/cratekit/cli/converge.py`
- Source: `u89.json`, row `C1_converge_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_is_converge_not_comparing_rather_than_a_match`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`

Old text:

```
            vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
            vocal_threshold=None,
```

### `u170.D1_kept_folded`

status: fold every old gate, the kept ones too

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D1_kept_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`

Old text:

```
            if aged is not None and aged.retirable:
```

New text:

```
            if aged is not None:
```

### `u170.D2_status_week`

status: threshold fixed at seven days, not the file's

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D2_status_week`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`

Old text:

```
    runs, folded = _run_report(timedelta(days=cfg.reports.open_gate_stale_days))
```

New text:

```
    runs, folded = _run_report(timedelta(days=7))
```

### `u170.D3_open_runs_short`

status: open_runs leaves the folded gates out

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D3_open_runs_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`

Old text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")) + folded,
```

New text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")),
```

### `u170.D4_line_dropped`

status: fold the gates and print no line for them

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D4_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`
  - `tests/test_run_retire.py::test_the_collapsed_line_names_the_dates_it_spans_and_reaches_a_person`

Old text:

```
    if old and older_than is not None:
```

New text:

```
    if False:
```

### `u211.C1_doctor_closed_is_a_note`

doctor rekordbox.closed: report an unconfirmed absence as OK rather than as a note

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u211.json`, row `C1_doctor_closed_is_a_note`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_doctor.py`
- Collected: 463 against a baseline of 463
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`

Old text:

```
            status=Status.INFO,
            detail=(
                f"{exc.cause.message}. Every database write refuses until the scan "
```

New text:

```
            status=Status.OK,
            detail=(
                f"{exc.cause.message}. Every database write refuses until the scan "
```

### `u211.C2_doctor_paths_take_no_copy`

doctor library.paths_resolved: let the unconfirmed refusal escape the check, so the rescue files it as a check that did not complete

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u211.json`, row `C2_doctor_paths_take_no_copy`
- Moved: U303 split cli/doctor.py and moved the paths check, verbatim but for its comment, to cli/doctor_library.py, which the same doctor tests import through the hub; the except clause is the same guard, narrowed the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_doctor.py`, `tests/test_paths_resolved.py`
- Collected: 514 against a baseline of 514
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`

Old text:

```
    except processes.AbsenceUnconfirmed as exc:
        # No copy over an unconfirmed absence (U211), a note as in rekordbox.closed.
```

New text:

```
    except LookupError as exc:
        # No copy over an unconfirmed absence (U211), a note as in rekordbox.closed.
```

### `r745-b.C1_pending_name_accepted`

_refuse_destination: accept a name the pending scan reads as an intake file

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C1_pending_name_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_favorites.xml]`
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_inboxed.xml]`
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_synced.xml]`

Old text:

```
        if name.endswith(suffix):
```

New text:

```
        if False:
```

### `r745-b.C3_create_not_exclusive`

_write_new: open for writing, replacing what is there. The composite for C2

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C3_create_not_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_file_that_appears_after_the_check_is_refused_by_the_write`
  - `tests/test_export_collection.py::test_a_file_that_came_and_went_is_still_refused_as_taken`

Old text:

```
open(destination, "xb")
```

New text:

```
open(destination, "wb")
```

### `r745-b.C4_torn_file_left`

_write_new: leave the file a failed write created

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C4_torn_file_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made`

Old text:

```
                destination.unlink()
```

New text:

```
                pass
```

### `r745-b.C5_made_folders_left`

_write_new: leave the folders a failed write made

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C5_made_folders_left`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made`

Old text:

```
                path.rmdir()
```

New text:

```
                pass
```

### `r745-b.C6_folder_not_asked_before_the_copy`

_refuse_destination: do not ask the folder before the database is copied

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C6_folder_not_asked_before_the_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied`

Old text:

```
    _refuse_unwritable_folder(destination)
```

New text:

```
    pass
```

### `r745-b.C8_live_database_opened`

_read: open the configured database itself, with no copy and no check that rekordbox is closed

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C8_live_database_opened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_rekordbox_or_its_agent_running_is_refused_and_nothing_is_written[rekordbox_agent_running]`
  - `tests/test_export_collection.py::test_rekordbox_or_its_agent_running_is_refused_and_nothing_is_written[rekordbox_running]`
  - `tests/test_export_collection.py::test_the_configured_database_is_never_opened_and_is_left_byte_for_byte`

Old text:

```
    with rb_writer.read_only_copy(database, cfg=cfg) as db:
```

New text:

```
    with __import__("contextlib").closing(
        rb_writer.open_db(database, require_closed=False, check_app_version=False, cfg=cfg)
    ) as db:
```

### `r745-c.C2_existing_file_not_checked_first`

_refuse_destination: drop the check ahead of the copy. Measured again after the test its zero bought

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-c.json`, row `C2_existing_file_not_checked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_existing_file_is_refused_before_the_database_is_copied`

Old text:

```
    if os.path.lexists(destination):
        raise _taken(destination)
```

New text:

```
    if False:
        raise _taken(destination)
```

### `r745-c.C7_a_file_taken_for_a_folder`

_refuse_unwritable_folder: do not ask whether the nearest ancestor is a folder. Measured again after the assertion its zero bought

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-c.json`, row `C7_a_file_taken_for_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied`

Old text:

```
    if not nearest.is_dir():
```

New text:

```
    if False:
```

### `r773-b.C10_summary_remapped_zero`

summary: report no location placed by a rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C10_summary_remapped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`

Old text:

```
                "locations_remapped": document.remapped,
```

New text:

```
                "locations_remapped": 0,
```

### `r773-b.C1_no_rule_handed_to_the_emitter`

_read: hand the emitter an empty prefix map, which is the export sitting 19 measured

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C1_no_rule_handed_to_the_emitter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        prefix_map=[
            locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()
        ],
```

New text:

```
        prefix_map=[],
```

### `r773-b.C2_root_not_the_library_root`

_read: hand the emitter the filesystem root as the library root

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C2_root_not_the_library_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_library_recorded_where_it_is_mounted_has_nothing_to_place`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`

Old text:

```
        root=cfg.library.root,
```

New text:

```
        root="/",
```

### `r773-b.C3_warning_not_given`

_warnings: give no warning over rows under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C3_warning_not_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes0-rule (3 under /a/b), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    if omitted.unmapped_paths:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
```

New text:

```
    if False:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
```

### `r773-b.C4_warning_counts_prefixes_as_rows`

_warnings: open the warning with the number of prefixes where the number of rows goes

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C4_warning_counts_prefixes_as_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes0-rule (3 under /a/b), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
                    f"{len(omitted.unmapped_paths)} track(s) record a path under "
```

New text:

```
                    f"{len(omitted.unmapped_prefixes)} track(s) record a path under "
```

### `r773-b.C5_prefix_cap_two`

_NAMED_PREFIXES: name two prefixes where three are named

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C5_prefix_cap_two`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`

Old text:

```
_NAMED_PREFIXES = 3
```

New text:

```
_NAMED_PREFIXES = 2
```

### `r773-b.C6_rest_of_the_prefixes_not_counted`

_warnings: never say how many prefixes were not named

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C6_rest_of_the_prefixes_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`

Old text:

```
        if more > 0:
            listed +=
```

New text:

```
        if False:
            listed +=
```

### `r773-b.C7_check_always_ok`

export.locations: report ok whatever is under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C7_check_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            status="ok" if not omitted.unmapped_paths else "info",
        ),
        _check(
            "export.tempo",
```

New text:

```
            status="ok",
        ),
        _check(
            "export.tempo",
```

### `r773-b.C8_summary_unmapped_zero`

summary: report no track under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C8_summary_unmapped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
                "tracks_under_no_rule": len(omitted.unmapped_paths),
```

New text:

```
                "tracks_under_no_rule": 0,
```

### `r773-b.C9_summary_left_zero`

summary: report no location left to a rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C9_summary_left_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
                "locations_left_to_a_rule": len(omitted.left_to_rule),
```

New text:

```
                "locations_left_to_a_rule": 0,
```

### `r1349.E2_open_left`

record (existing): the open gate left open after it is answered

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `E2_open_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 10 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide`
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_an_answered_run_two_days_old_is_not_blocked`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_run_retire.py::test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again`
  - `tests/test_run_retire.py::test_a_wider_threshold_retires_fewer`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`
  - `tests/test_run_retire.py::test_retire_reads_its_default_threshold_from_the_file`
  - `tests/test_run_retire.py::test_retire_says_nothing_about_an_old_run_already_answered`

Old text:

```
    if state.open_gate == spec.name:
        state.open_gate = None


def blocked_by
```

New text:

```
    if False:
        state.open_gate = None


def blocked_by
```

### `r1349.E3_offer_unrecorded`

require (existing): the offer never recorded when the gate is reached

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `E3_offer_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 47 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.all]`
  - `tests/test_gate_not_reached.py::test_a_gate_offered_and_answered_takes_a_new_answer_over_its_offer`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`
  - ... and 32 more, see the JSON sidecar

Old text:

```
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest
```

New text:

```
        if False:
            self.state.offers[spec.name] = digest
```

### `r1349.N4_open_ignored`

record: the open gate clause dropped, so a gate reached with no digest and left open is refused

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N4_open_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 15 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_admits_a_verb_carrying_two_gates[explicit-then-explicit]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[run.retire]`
  - `tests/test_gate_not_reached.py::test_a_gate_already_answered_takes_a_new_answer_once_the_run_waits_elsewhere`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide`
  - `tests/test_gate_siblings.py::test_an_answered_run_two_days_old_is_not_blocked`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_this_run_was_offered_no_digest`
  - `tests/test_run_retire.py::test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again`
  - `tests/test_run_retire.py::test_a_record_retire_cannot_read_is_said_and_not_dropped`
  - `tests/test_run_retire.py::test_a_wider_threshold_retires_fewer`
  - `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`
  - `tests/test_run_retire.py::test_retire_never_retires_its_own_run`
  - `tests/test_run_retire.py::test_retire_reads_its_default_threshold_from_the_file`
  - `tests/test_run_retire.py::test_retire_says_nothing_about_an_old_run_already_answered`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `u168.C12_argv_not_saved`

RunState.to_json: drop the command line from the saved record

- File: `src/cratekit/cli/gates.py`
- Source: `u168.json`, row `C12_argv_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`, `tests/test_gate_pins.py`
- Collected: 1035 against a baseline of 1035
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_a_continuation_that_refuses_answers_with_its_refusal_and_keeps_the_answer`
  - `tests/test_run_decide_continue.py::test_a_session_answers_and_mints_in_one_command_with_no_actor_given`
  - `tests/test_run_decide_continue.py::test_the_continuation_is_given_the_arguments_its_first_invocation_recorded`

Old text:

```
        if self.argv is not None:
            record["argv"] = list(self.argv)
```

New text:

```
        if False:
            record["argv"] = list(self.argv)
```

### `u170.G2_idle_from_start_only`

idle_since: age from created alone, so a resumed run is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G2_idle_from_start_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_exactly_at_the_threshold_is_not_yet_old`
  - `tests/test_run_retire.py::test_a_run_resumed_recently_is_not_old_however_long_ago_it_started`
  - `tests/test_run_retire.py::test_an_answer_is_stale_once_a_planned_run_is_resumed_even_if_it_stays_old`

Old text:

```
    return written if started is None else max(started, written)
```

New text:

```
    return written if started is None else started
```

### `u170.G3_idle_from_write_only`

idle_since: age from the record's write alone, so a copied record with an old date is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G3_idle_from_write_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_run_started_recently_is_not_old_whatever_its_file_says`

Old text:

```
    return written if started is None else max(started, written)
```

New text:

```
    return written
```

### `u170.G4_unstattable_is_old`

idle_since: a record whose time cannot be read is as old as the epoch

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G4_unstattable_is_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_record_whose_time_cannot_be_read_is_never_old`

Old text:

```
        return datetime.now(timezone.utc)
```

New text:

```
        return datetime.fromtimestamp(0, tz=timezone.utc)
```

### `u170.G5_no_abort_retired`

old_gate: drop the no abort refusal, so sync.pair gates are planned

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G5_no_abort_retired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`

Old text:

```
    elif RETIRE_OPTION not in spec.options:
```

New text:

```
    elif False:
```

### `u170.G6_missing_verb_branch`

old_gate: drop the missing verb reason, so the fallback reason speaks for it

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G6_missing_verb_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_whose_verb_is_gone_is_old_and_kept`

Old text:

```
    if owner is None:
        kept: str | None = f"{state.verb} is not a verb in this build"
    elif spec is None:
```

New text:

```
    if owner is None and False:
        kept: str | None = f"{state.verb} is not a verb in this build"
    elif spec is None:
```

### `u170.G8_malformed_stamp`

_instant: a malformed created stamp raises instead of reading as unknown

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G8_malformed_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1739 against a baseline of 1739
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_hand_edited_start_stamp_is_aged_by_the_records_last_write`

Old text:

```
    except (TypeError, ValueError):
        return None
    return moment if
```

New text:

```
    except TypeError:
        return None
    return moment if
```

### `u183.M16_record_written_only_when_set`

RunState.to_json: write related_runs always, so every record moves

- File: `src/cratekit/cli/gates.py`
- Source: `u183.json`, row `M16_record_written_only_when_set`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_gate_pins.py`, `tests/test_run_decide_continue.py`, `tests/test_run_retire.py`
- Collected: 127 against a baseline of 127
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_land_run_that_recorded_no_pass_is_refused_and_says_why`
  - `tests/test_sync_land.py::test_a_record_with_no_related_runs_is_the_record_it_was_and_one_with_them_round_trips`

Old text:

```
        if self.related_runs:
            record["related_runs"]
```

New text:

```
        if True:
            record["related_runs"]
```

### `u183.M17_record_read_back`

RunState.from_json: read related_runs as empty, so a saved pass is lost on load

- File: `src/cratekit/cli/gates.py`
- Source: `u183.json`, row `M17_record_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_gate_pins.py`, `tests/test_run_decide_continue.py`
- Collected: 86 against a baseline of 86
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_land_run_whose_pass_no_intake_job_carries_is_refused_not_continued`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_record_with_no_related_runs_is_the_record_it_was_and_one_with_them_round_trips`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
                {str(role): str(run) for role, run in data["related_runs"].items()}
                if isinstance(data.get("related_runs"), dict)
```

New text:

```
                {}
                if isinstance(data.get("related_runs"), dict)
```

### `u183.M18_load_refuses_non_object`

gates.load: drop the refusal of a record that is not a JSON object

- File: `src/cratekit/cli/gates.py`
- Source: `u183.json`, row `M18_load_refuses_non_object`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_run_retire.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_is_the_gates_own_refusal`

Old text:

```
    if not isinstance(raw, dict):
        raise CratekitError(
```

New text:

```
    if False:
        raise CratekitError(
```

### `u49-author.G1_an_explicit_gate_takes_an_inline_answer_again`

Restore the recorded-is-None qualifier this unit removed, so a flag can overturn a recorded abort and mint the acknowledgment

- File: `src/cratekit/cli/gates.py`
- Source: `u49-author.json`, row `G1_an_explicit_gate_takes_an_inline_answer_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`

Old text:

```
        if inline is not None and spec.explicit:
```

New text:

```
        if inline is not None and spec.explicit and recorded is None:
```

### `u274.H1_drive_not_entered`

run_job: never enter the worker's per drive holder

- File: `src/cratekit/cli/handlers.py`
- Source: `u274.json`, row `H1_drive_not_entered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 17 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_engine_opens_a_workers_drive_once_and_closes_it_on_a_park`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    with held() if held is not None else nullcontext() as holding:

```

New text:

```
    with nullcontext() as holding:

```

### `u274.H2_warnings_dropped`

run_job: drop what the holder noted at its close, so a session the keychain refused is said nowhere

- File: `src/cratekit/cli/handlers.py`
- Source: `u274.json`, row `H2_warnings_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
    if noted:
        result.warnings = (*result.warnings, *noted)

```

New text:

```
(empty)
```

### `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound`

The handler key goes back to declaring no worker, which is the state this whole unit exists to leave

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R39_tag_folder_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 345 against a baseline of 345
- Kills: 41 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
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
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    "tag.folder": "cratekit.tagging.cli:handle",
```

New text:

```
(empty)
```

### `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound`

The same for the correction verb

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R40_tag_retag_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 345 against a baseline of 345
- Kills: 21 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
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
  - ... and 6 more, see the JSON sidecar

Old text:

```
    "tag.retag": "cratekit.tagging.retag_cli:handle",
```

New text:

```
(empty)
```

### `u182.M13_identity_parse`

playlist_identity: key on the raw source instead of the pass's reading

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M13_identity_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_sync_land.py`
- Collected: 155 against a baseline of 155
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_the_job_verbs_read_a_playlist_as_the_sweep_records_it`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        return catalogue.playlist_id(source)
```

New text:

```
        return source
```

### `r1499.L01_go_arrival_after_tail`

label sync: no check after the go's name apply, so an arrival is planned into the go's landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L01_go_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`

Old text:

```
        if changed is not None:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

New text:

```
        if False:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

### `r1499.L02_go_kept_after_arrival`

_kept: the go keeps its record although something arrived

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L02_go_kept_after_arrival`
- Moved: Same _kept guard; U298 replaced this copy of _changed_said with tail.changed_said, which only rewords the line under the condition the row mutates
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_a_gos_landing_is_planned_refuses_it`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_gos_tail_that_fails_while_a_download_arrives_says_its_record_was_not_kept`

Old text:

```
    if changed is not None:
        return [_unkept(folder, job, tail.changed_said(changed))]
```

New text:

```
    if False:
        return [_unkept(folder, job, tail.changed_said(changed))]
```

### `u190.L10_rest_of_tail_after_a_step_gate`

_attended: name nothing after a tail step's own gate, so the rest of the tail is left unsaid

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L10_rest_of_tail_after_a_step_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
        after = tuple(f"then: {one}" for one in _commands(folder, landing, stop.step)[1:])
```

New text:

```
        after = ()
```

### `u190.L11_done_keeps_the_go_outcome`

label_sync: end a landing that planned nothing as NO_OP, hiding the download the go made

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L11_done_keeps_the_go_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
        outcome=envelope.outcome,
```

New text:

```
        outcome=Outcome.NO_OP,
```

### `u190.L1_no_tail_returns_untouched`

label_sync: run the chain over a go that names no tail

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L1_no_tail_returns_untouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 146 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[label.sync]`
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv3-go with --answer]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv5-goes with --answer pick]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv6---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv7---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_label_with_nothing_new_is_not_asked_and_a_run_with_nothing_to_ask_says_so`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_labels_own_offer_bounds_a_first_question`
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - ... and 131 more, see the JSON sidecar

Old text:

```
    if land is None:
        return envelope
    cfg
```

New text:

```
    if land is None:
        land = {"folder": "/nowhere", "pass": "none"}
    cfg
```

### `u190.L2_land_of_needs_a_mapping`

_land_of: read the go's report without its key, so no tail is ever run

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L2_land_of_needs_a_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 56 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - ... and 41 more, see the JSON sidecar

Old text:

```
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
```

New text:

```
    land = report.get("tail") if isinstance(report, Mapping) else None
```

### `u190.L3_landing_carries_manifest`

_landing_args: drop the manifest, so the landing files the label's rows under no label

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L3_landing_carries_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        *(["--manifest", str(manifest)] if isinstance(manifest, str) and manifest else []),
```

New text:

```
        *([] if isinstance(manifest, str) and manifest else []),
```

### `u190.L4_landing_carries_pass`

_landing_args: drop the pass, so the landing's intake file is named for nothing the go named

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L4_landing_carries_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        "--pass",
        str(land["pass"]),
    ]
```

New text:

```
    ]
```

### `u190.L5_land_stop_rekordbox_visit`

_attended: follow the landing's gate with the next tail command rather than the rekordbox visit

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L5_land_stop_rekordbox_visit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it`

Old text:

```
    if stop.step == tail.LAND:
        after: Sequence[str] = tail.REKORDBOX_STEPS
```

New text:

```
    if False:
        after: Sequence[str] = tail.REKORDBOX_STEPS
```

### `u190.L6_way_on_from_the_stopped_step`

_commands: name the whole tail from its first step, so a person reruns steps that succeeded

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L6_way_on_from_the_stopped_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
tail.STEPS[tail.STEPS.index(step):]
```

New text:

```
tail.STEPS[0:]
```

### `u190.L7_pending_id_names_the_go`

_attended: name the pending action for the landing's run rather than the go's

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L7_pending_id_names_the_go`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it`

Old text:

```
        id=f"label-sync-{ctx.run.run_id}",
```

New text:

```
        id=f"label-sync-{chain.summary.get('gate_run')}",
```

### `u190.L9_verify_verb_by_step`

_attended: name the landing as the verb to verify whatever step stopped

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L9_verify_verb_by_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1225 against a baseline of 1225
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
        verify_verb=tail.LAND_VERB if stop.step == tail.LAND else ctx.entry.name,
```

New text:

```
        verify_verb=tail.LAND_VERB,
```

### `u239.L01_remember_land_only`

_remember: record a gate stop at any step as the landing, so a restamp gate is taken for it

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L01_remember_land_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`

Old text:

```
    if not (stop.step == tail.LAND and stop.cause.reason == tail.GATE_STOP and landed):
```

New text:

```
    if not (stop.cause.reason == tail.GATE_STOP and landed):
```

