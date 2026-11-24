# Mutation table: u333-replay-before-4

Measured by `scripts/mutate.py` on 2026-11-24 05:14 UTC, branch `HEAD` at `35e9a825`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 437.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:14 UTC for commit `35e9a825cd73`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 57, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u177.C1_label_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `u177.C2_no_label_filed` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 46 | 1 | killed |
| `r1677.L2_rehearsal_room_silent` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `r1677.L3_rehearsal_other_failure_sound` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `r501-b.L1_unretired_name` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 34 | 3 | killed |
| `r677-b.V4_after_the_stale_test` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `r677.V1_no_preflight_before_the_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 7 | killed |
| `r677.V2_preflight_on_a_plan_of_nothing` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `r677.V3_refusal_never_replaces_the_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 5 | killed |
| `r677.V5_preflight_raises_directly` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `r677.V6_manifest_rows_not_handed_over` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `r770-b.B1_landing_never_takes_the_native_path` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 44 | 28 | killed |
| `u110-b.B1_pass_names_file` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 5 | killed |
| `u110-b.B2_name_names_file` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 81 | 18 | killed |
| `u110-b.B3_check_pass` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 5 | killed |
| `u110-b.B4_recheck_xml` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u110-b.B5_recheck_native` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 44 | 1 | killed |
| `u110-b.B6_intake_lock` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u110-b.B7_name_overrides` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 125 | 27 | killed |
| `u110-b.B8_shown_playlist` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u113-b.B7_digest_blind_to_split` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u113-b.B8_pending_names_unheld` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u120.C2_hearts_not_claimed` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 13 | 10 | killed |
| `u127.L6_bridge_ignores_calibration` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u128-b.B3_owned_unresolved_at_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 4 | killed |
| `u128.L1_bridge_warning_unsaid` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `u146-c.L2_empty_landing_no_op` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 12 | 4 | killed |
| `u156.L23_label_beside_manifest` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u156.L24_label_on_the_bridge` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u162.L10_interrupt_cancel` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u162.L12_rehearsal_equal` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u162.L1_bridge_refusal` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u162.L2_area_plan_compare` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u162.L4_occupied_hold` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u162.L6_gridless_read_back` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u162.L7_identified_read_back` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u162.L8_success_witness` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u162.L9_kept_area_named` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 4 | killed |
| `u164.H1_watch_recorded` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u164.H2_scratch_folder` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 18 | killed |
| `u165.L3_filing_tail` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 10 | 3 | killed |
| `u177.C3_flag_beside_label` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u188.M10_detail_mapped_dropped` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u188.M11_fields_last_part` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M12_fields_keep_indices` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M13_fields_repeated` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M1_stored_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M2_scratch_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M3_live_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M4_staging_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 18 | killed |
| `u188.M6_mapped_as_lines` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M7_signs_swapped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M8_fields_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M9_pairs_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u307.R20_land_only_by_default` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 10 | 5 | killed |
| `u307.R21_unrunnable_reason_lost` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u307.R4_land_cli_getattr_answers_none` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 116 | 23 | killed |
| `u331.S06_landing_room_check_dropped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u72-b.M18_refused_unmarked` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M20_shown_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M21_empty_to_engine` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M22_listing_without_isdir` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M10_default_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 19 | killed |
| `u72.M1_abort_applies` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M2_empty_plan_applied` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M3_digest_drops_where` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M4_digest_drops_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M5_digest_drops_export` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M6_digest_drops_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M7_gate_digest_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 23216 | 5 (promoted) | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-c.C6_gate_manifest_bytes` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-c.C7_digest_handed_to_engine` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-c.C8_unfiled_rows_warned` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `r770-b.B2_gate_asked_before_the_acknowledgment` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `r770-b.B3_an_abort_writes` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `u120.C1_no_skip_note` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 13 | 2 | killed |
| `u126.P3_gate_fact` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 4 | killed |
| `u127.L1_screen_line_blind` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.L2_items_carry_no_vox` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 6 | killed |
| `u127.L3_totals_from_writer` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.L4_missing_unsaid` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.L5_unscored_unsaid` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.L7_land_warnings_unsaid` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 60 | 6 | killed |
| `u128-b.N3_native_owned_not_found` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 3 | killed |
| `u128.L2_native_warning_unsaid` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 2 | killed |
| `u146-c.L3_gate_asked_for_nothing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-c.L4_missing_source_refuses` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u153.L1_facts_colour_count` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u153.L3_notes_colour_skipped` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 13 | 1 | killed |
| `u157.L1_selection_counts` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 2 | killed |
| `u157.L2_blocked_unnamed` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 1 | killed |
| `u161.L1_landing_pins_nothing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P6_screen_drops_path` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 44 | 2 | killed |
| `u165.L1_bridge_skip` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 54 | 2 | killed |
| `u165.L2_land_only` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 54 | 3 | killed |
| `u165.L4_files_into` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 10 | 2 | killed |
| `u166.A11_warning_names_batch` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 63 | 3 | killed |
| `u177.C4_flag_ignored` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 46 | 4 | killed |
| `u181.L1_half_is_a_warning` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u181.L2_coefficient` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u307.R22_colour_notes_drop_held` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 2 | killed |
| `u319.M8_ok_on_any_field` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 41 | 2 | killed |
| `u319.M9_warning_drops_the_short_path` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 2 | killed |
| `u954.M1_no_dyn_case` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 3 | killed |
| `u954.M2_every_row_dyn_case` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 1 | killed |
| `u954.M3_mixed_order` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 1 | killed |
| `u954.M5_auto_step_condition_landing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 41 | 2 | killed |
| `u954.M7_untagged_rows_order` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 17 | 1 | killed |
| `r432-a.A1_key_casefold` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `r432-a.A3_lock_never_taken` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 11 | killed |
| `r432-a.A5_not_retryable` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `r432-a.A8_holder_left_out` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `r432-b.A4c_lock_outlives_its_with` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 5 | killed |
| `r677.E1_export_asked_before_the_library` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 61 | 32 | killed |
| `r677.E2_library_check_dropped` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `r677.E3_intake_file_check_dropped` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 3 | killed |
| `r746-b.N8_unsupported_file_moved_anyway` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `r746-b.N9_placement_check_dropped_from_the_screen` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `r770-c.C3_failure_past_the_gate_loses_its_reason` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r770-c.C4_failure_past_the_gate_loses_its_remedy` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 33 | 1 | killed |
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 20 | 4 | killed |
| `u110-c.C7_intake_lock_prefix` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 47 | 13 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 20 | 1 | killed |
| `u113-b.B5_export_clash_unasked` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 26 | 1 | killed |
| `u113-b.B6_root_names_unheld` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 26 | 1 | killed |
| `u113-c.C6_names_checked_after_moves` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 16 | 1 | killed |
| `u128-b.B1_engine_stale_unchecked` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 26 | 1 | killed |
| `u128-b.B2_foreign_host_indexed` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 26 | 1 | killed |
| `u164.W1_apply_folder` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 50 | 24 | killed |
| `u164.W2_preflight_target` | `src/cratekit/intake/landing.py` | maintainer | 1 file(s) | 6 | 1 | killed |
| `u307.R6_refuse_past_drops_inner_message` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 77 | 4 | killed |
| `u72-b.M23_listing_unfiltered` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-a.A6_no_landed_file_guard` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 27 | 2 | killed |
| `r502-a.G5_no_adjudicate` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 4 | killed |
| `r502-a.G6_no_mount_guard` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r502-a2.G7_frozen_config` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r502-b.E2_nothing_written_refusal` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 1 | killed |
| `r502-b.G10_since_keys_swapped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 5 | killed |
| `r502-b.G12_since_check_detail` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r502-b.G9_missing_count_stale` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r502-b2.G13_written_line_for_gained` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r503-a.G10_owned_key` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 30 | killed |
| `r503-a.G1_no_lookup` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `r503-a.G2_found_is_answered` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r503-a.G4_offered_not_decremented` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `r503-a.G5_state_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r503-a.G6_answered_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `r503-a.G7_answered_read_as_since` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `r503-a.G8_rejected_not_kept` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r503-a.G9_answered_last` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r503-b.E2_offered_listed` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r503-b.G11_summary` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `r503-b.G12_answered_check` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r503-b.G13_offered_check` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r503-b.G14_no_gone` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r503-b.G15_no_new` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r503-b.G16_json_uncaught` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `r503-b.G17_no_hint` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u110-c.C5_missing_hint` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u207.I1_missing_never_screens` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u212.M10_left_out` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u212.M1_staged_match` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 5 | killed |
| `u212.M2_own_rows_both` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 3 | killed |
| `u212.M3_own_rows_by_id` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u212.M4_own_rows_by_isrc` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u212.M5_unread_is_empty` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u212.M6_absent_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u212.M7_outcome_staged` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u212.M8_summary_count` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 4 | killed |
| `u212.M9_unread_status` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 9 | 1 | killed |
| `u307.R12_summary_head_written_zero` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 107 | 23 | killed |
| `u307.R13_named_by_isrc_resolves_unasked` | `src/cratekit/intake/missing_cli.py` | user | 2 file(s) | 48 | 5 | killed |
| `u69-b.M10_out_not_a_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M12_unlisted_status` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M16_next_command` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u69-b.M17_lists_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `u69-b.M18_inner_cause` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M19_resume_step` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M1_handler_key` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M2_succeeded_only` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u69.M4_report_coverage` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M5_by_count` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M6_state_word` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73-b.B2_every_ref_kept` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73-b.B3_first_source_wins` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A10_every_job_skipped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A1_blank_run` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A2_library_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A3_run_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A4_intake_key_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A5_oldest_first` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u73.A7_open_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A8_failed_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A9_skip_failed_ignored` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u78-a.A3_several_listed` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 2 | killed |
| `u78-a.A5_outage_read_as_none` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 1 | killed |
| `u78-a.A6_blank_id_dropped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 1 | killed |
| `u78-b.B1_unwritable_refuses_whole` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 2 | killed |
| `u78-b.B3_ids_unsorted` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 1 | killed |
| `u78-d.A4_cratekit_error_passthrough_again` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 8 | 1 | killed |
| `u79-c.C2_owned_row_searched` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-c.C3_accepted_held_listed_again` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-c.C4_nothing_found_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-c.C5_foreign_ref_names_a_row` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-c.C6_isrc_named_keeps_origin` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-c.C7_fixed_name` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 10 | killed |
| `u79-c.C8_asked_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 50 | 1 | killed |
| `r1037.N1_landed_not_recorded` | `src/cratekit/intake/native.py` | user | 2 file(s) | 86 | 33 | killed |
| `r1037.N2_joined_not_made` | `src/cratekit/intake/native.py` | user | 1 file(s) | 42 | 5 | killed |
| `r1037.N3_identity_wrong` | `src/cratekit/intake/native.py` | user | 1 file(s) | 42 | 21 | killed |
| `r1037.N4_size_not_read` | `src/cratekit/intake/native.py` | user | 1 file(s) | 42 | 12 | killed |
| `r1037.N5_count_before_commit` | `src/cratekit/intake/native.py` | user | 1 file(s) | 42 | 1 | killed |
| `r1037.N6_before_empty` | `src/cratekit/intake/native.py` | user | 1 file(s) | 42 | 5 | killed |
| `r1844.N13_landing_writes_no_uuid` | `src/cratekit/intake/native.py` | user | 1 file(s) | 42 | 5 | killed |
| `r746-b.N3_folder_path_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `r746-b.N4_device_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `r777.N16_pass_not_recorded` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `r923.N1_landing_sets_nothing` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u113-c.C1_native_batch_always` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 6 | killed |
| `u113-c.C2_native_batch_keeps_claimed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 7 | killed |
| `u113-c.C3_native_found_by_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u113-c.C4_native_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 3 | killed |
| `u115.F1_landing_keeps_random_id` | `src/cratekit/intake/native.py` | user | 3 file(s) | 93 | 27 | killed |
| `u120.N3_identity_without_hearts` | `src/cratekit/intake/native.py` | user | 1 file(s) | 13 | 1 | killed |
| `u126.F3_counts_undigested` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u126.P2_not_shown` | `src/cratekit/intake/native.py` | user | 2 file(s) | 77 | 4 | killed |
| `u126.R1_binding_value_kept` | `src/cratekit/intake/native.py` | user | 4 file(s) | 106 | 37 | killed |
| `u126.R2_fill_if_null` | `src/cratekit/intake/native.py` | user | 4 file(s) | 106 | 37 | killed |
| `u126.R3_check_skipped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 2 | killed |
| `u126.R5_read_back_file_id` | `src/cratekit/intake/native.py` | user | 4 file(s) | 106 | 37 | killed |
| `u126.S1_file_id_kept` | `src/cratekit/intake/native.py` | user | 4 file(s) | 106 | 38 | killed |
| `u126.S2_defaults_left_null` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u127-b.N6b_digest_blind_to_vox` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.N10_record_silent` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.N11_missing_unreported` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.N12_unscored_dropped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.N14_read_back_skipped` | `src/cratekit/intake/native.py` | user | 2 file(s) | 49 | 4 | killed |
| `u127.N7_digest_blind_to_cut` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.N8_tag_never_written` | `src/cratekit/intake/native.py` | user | 2 file(s) | 49 | 6 | killed |
| `u127.N9_tag_every_added` | `src/cratekit/intake/native.py` | user | 5 file(s) | 122 | 50 | killed |
| `u128-b.N1_native_owned_unwritten` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 3 | killed |
| `u128-b.N2_native_record_no_pass` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 2 | killed |
| `u146-c.N2_owned_not_written` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-e.N3_owned_out_of_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u150.F2_record_provider` | `src/cratekit/intake/native.py` | user | 1 file(s) | 46 | 1 | killed |
| `u153.N1_restamp_id_text` | `src/cratekit/intake/native.py` | user | 2 file(s) | 25 | 8 | killed |
| `u153.N3_landing_colour_owned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u156.L18_digest_native` | `src/cratekit/intake/native.py` | user | 1 file(s) | 46 | 3 | killed |
| `u156.L19_write_called` | `src/cratekit/intake/native.py` | user | 1 file(s) | 46 | 17 | killed |
| `u156.L20_recorded` | `src/cratekit/intake/native.py` | user | 1 file(s) | 46 | 3 | killed |
| `u157.N2_digest_rows` | `src/cratekit/intake/native.py` | user | 1 file(s) | 17 | 1 | killed |
| `u157.N3_no_write` | `src/cratekit/intake/native.py` | user | 1 file(s) | 17 | 4 | killed |
| `u157.N4_trust_the_writer` | `src/cratekit/intake/native.py` | user | 1 file(s) | 17 | 1 | killed |
| `u157.N5_no_record` | `src/cratekit/intake/native.py` | user | 1 file(s) | 17 | 1 | killed |
| `u161.P1_path_back_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 3 | killed |
| `u161.P2_parent_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 2 | killed |
| `u161.P3_file_name_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P4_device_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P5_master_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.S1_playlist_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.S2_columns_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u163.W12_readback_active` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W13_identified_words` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W14_album_artist_link` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u163.W4_year_written` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W7_unmoved` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W8_mint_once` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W9_creations_named` | `src/cratekit/intake/native.py` | user | 2 file(s) | 62 | 23 | killed |
| `u164.R1_record_filed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 75 | 7 | killed |
| `u165.N1_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 10 | 1 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 5 file(s) | 120 | 13 | killed |
| `u166.A5_present_rows_too` | `src/cratekit/intake/native.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.A6_always_create` | `src/cratekit/intake/native.py` | user | 1 file(s) | 14 | 2 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 4 file(s) | 104 | 4 | killed |
| `u166.A8_digest_key` | `src/cratekit/intake/native.py` | user | 1 file(s) | 14 | 1 | killed |
| `u307.R23_batch_order_keeps_claimed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 16 | 7 | killed |
| `u954.M8_no_category_order` | `src/cratekit/intake/native.py` | user | 1 file(s) | 17 | 1 | killed |
| `r746-b.N2_base_drive_swap_disabled` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 44 | 2 | killed |
| `r746-b.N5_present_file_planned_as_an_add` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 44 | 3 | killed |
| `r770-d.C7_unresolved_target_planned_as_an_add` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 33 | 1 | killed |
| `r777.N15_any_pass` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 44 | 1 | killed |
| `u113-c.C5_removed_node_holds_name` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 16 | 1 | killed |
| `u120.N4_skipped_is_raised` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 13 | 2 | killed |
| `u126.F1_read_always` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 44 | 1 | killed |
| `u126.P1_no_read` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 77 | 7 | killed |
| `u127.N1_cut_strict` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 49 | 2 | killed |
| `u127.N2_every_add_tagged` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 16 | 5 | killed |
| `u127.N3_default_cut_when_uncalibrated` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 49 | 2 | killed |
| `u127.N4_unreadable_refuses` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.N5_no_category_check` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 16 | 1 | killed |
| `u128-b.N4_native_dropped_left_lost` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 16 | 1 | killed |
| `u146-c.N1_owned_held_planned` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-c.N4_owned_needs_a_heart_file` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 12 | 1 | killed |
| `u157.N1_writable_unasked` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 17 | 1 | killed |
| `u163.W10_search_convention` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W11_search_tie` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W1_words_planned` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 62 | 10 | killed |
| `u163.W2_first_value` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W3_year_digits` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 18 | 2 | killed |
| `u163.W5_album_artist_mint` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 18 | 1 | killed |
| `u163.W6_album_by_artist` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 18 | 1 | killed |
| `u166.A1_parent_check` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.A2_removed_check` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 14 | 2 | killed |
| `u166.A3_plain_check` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 14 | 1 | killed |
| `u166.A9_reserved_batch` | `src/cratekit/intake/native_plan.py` | user | 1 file(s) | 14 | 1 | killed |
| `r1255.F1_refill_plan_unlisted` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A10_shared_playlist` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A11_pass_unknown` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A1_outside_inbox` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A2_mirror_is_first` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A3_gone_listed` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A4_others_excluded` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A5_unreadable` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A6_pre_u128_exact_name` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A7_pass_matched` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-a.A8_only_what_it_lacks` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 2 | killed |
| `u134-b.B1c_composite_short_write` | `src/cratekit/intake/refill.py` | maintainer | 1 file(s) | 13 | 7 | killed |
| `u134-b.B2c_composite_reversed_write` | `src/cratekit/intake/refill.py` | maintainer | 1 file(s) | 13 | 7 | killed |
| `u134-b.B4_record_on_success` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-b.B7_again_action` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u175.F1_bridge_name_unasked` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u175.F2_bridge_names_any_account` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u175.F3_analyze_asked` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 14 | 1 | killed |
| `u175.F4_bridge_names_any_state` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u175.F5_bridge_names_by_id_order` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1255.F2_refill_warning_wording` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `u134-b.B5_no_writes_no_op` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 13 | 3 | killed |
| `u134-b.B6_ack_before_gate` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 13 | 1 | killed |
| `u307.R10_refill_writing_watches_nothing` | `src/cratekit/intake/refill_cli.py` | user | 2 file(s) | 27 | 13 | killed |
| `u331.S09_rehearsal_origin_renamed` | `src/cratekit/intake/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u331.S10_check_engine_imports_analysis_at_top` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 57 | 2 | killed |
| `r1255.R1_rotation_unlisted_from_scan` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `r1255.R2_plan_carries_unlisted` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `u111-c.C3_inboxed_suffix` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-c.C4_removal_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 2 | killed |
| `u111-c.C5_move_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 2 | killed |
| `u111-c.C6_plan_taken_again` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-c.C7_old_creation_planned` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-d.C10_two_olds_refused` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-d.C9_committed_records_only` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `u113-c.C7_unproven_import_names` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 5 | 1 | killed |
| `u113-c.C9_earliest_name_wins` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 5 | 1 | killed |
| `u166.R2_rotate_reserved` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 14 | 1 | killed |
| `u175.R1_account_ids_unrecorded` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 16 | 2 | killed |
| `u214.M15_unread_is_not_none` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 2 | killed |
| `u214.M16_old_only_under_inbox` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `u214.M18_folder_unknown` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `u214.M19_folder_unread_reason` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `u214.M1_old_named_as_old` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 5 | killed |
| `u214.M20_unread_unlisted` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `u214.M2_left_row_count` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 4 | killed |
| `u214.M3_live_left_collected` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 8 | killed |
| `u214.M4_digest_without_count` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 1 | killed |
| `u214.M5_rotation_old_display` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 3 | killed |
| `u214.M6_live_old_display` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 3 | killed |
| `u214.M7_label_rows` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 27 | 2 | killed |
| `u307.R8_anchored_root_drops_cutover_step` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 44 | 2 | killed |
| `u329.W3_rotate_holds_a_permissive_copy` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 30 | 1 | killed |
| `r1255.R3_rotation_warning_gate` | `src/cratekit/intake/rotate_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `r1255.R4_rotation_warning_wording` | `src/cratekit/intake/rotate_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u111-d.D1_empty_plan_asks` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 1050 | 4 | killed |
| `u111-d.D2_ack_before_gate` | `src/cratekit/intake/rotate_cli.py` | user | 1 file(s) | 30 | 1 | killed |
| `r1017.M3_landing_open_read` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 29 | 1 | killed |
| `r1017.M4_landing_uncommitted_read` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 29 | 1 | killed |
| `r1017.M5_landing_any_job` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 29 | 2 | killed |
| `r1017.M6_oldest_first` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 29 | 1 | killed |
| `r1017.M7_names_not_deduplicated` | `src/cratekit/intake/set_playlist.py` | maintainer | 1 file(s) | 29 | 1 | killed |
| `u154.G10_read_back_path_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G11_kept_columns_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G14_reserved_folders_are_candidates` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G15_stored_target_under_mounted_path` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G17_refusal_before_rename_rewrapped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G1_policy_not_registered` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 5 | killed |
| `u154.G2_confinement_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 1 | killed |
| `u154.G3_rename_back_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 23 | 2 | killed |

## Zero rows and what they owe

- `u69-b.M16_next_command` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u146-e.N3_owned_out_of_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u177.C1_label_fold`

_read_label: drop the NFC fold, so one label spelled two ways makes two folders

- File: `src/cratekit/intake/label_filing.py`
- Source: `u177.json`, row `C1_label_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder`

Old text:

```
    named = _folded(str(stored or "").strip())

```

New text:

```
    named = str(stored or "").strip()

```

### `u177.C2_no_label_filed`

plan_for_tags: file a file with no label tag under an empty label, not under none

- File: `src/cratekit/intake/label_filing.py`
- Source: `u177.json`, row `C2_no_label_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`

Old text:

```
        if not label or year is None:
            unfiled.append(
                Unfiled(
                    target=str(target),
                    reason=landing.NO_LABEL,
                    sentence=(
                        f"{target.name} was filed under no "

```

New text:

```
        if label and year is None:
            unfiled.append(
                Unfiled(
                    target=str(target),
                    reason=landing.NO_LABEL,
                    sentence=(
                        f"{target.name} was filed under no "

```

### `r1677.L2_rehearsal_room_silent`

land_cli: a rehearsal check whose copy found no room is told as a failed integrity check

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L2_rehearsal_room_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`

Old text:

```
        if no_room is not None:
            raise no_room from failed
        sound = False
```

New text:

```
        sound = False
```

### `r1677.L3_rehearsal_other_failure_sound`

land_cli: a rehearsal check whose copy failed for another reason is reported sound, integrity ok without a check

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L3_rehearsal_other_failure_sound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`

Old text:

```
            raise no_room from failed
        sound = False
```

New text:

```
            raise no_room from failed
        sound = True
```

### `r501-b.L1_unretired_name`

land_cli.unretired_name: return the name unchanged, so sync mark cannot find its pass from a retired intake file

- File: `src/cratekit/intake/land_cli.py`
- Source: `r501-b.json`, row `L1_unretired_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_sync_mark_reads_the_same_pass_off_a_retired_intake_file[RUN_synced_inboxed.xml.imported-2]`
  - `tests/test_intake_imported.py::test_sync_mark_reads_the_same_pass_off_a_retired_intake_file[RUN_synced_inboxed.xml.imported]`
  - `tests/test_intake_imported.py::test_the_retired_name_is_out_of_the_pending_scan_and_reads_back`

Old text:

```
    return _RETIRED_TAIL.sub("", name)
```

New text:

```
    return name
```

### `r677-b.V4_after_the_stale_test`

any gate refusal, a stale answer included, is replaced by the preflight refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677-b.json`, row `V4_after_the_stale_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
```

New text:

```
        if unusable is not None:
```

### `r677.V1_no_preflight_before_the_gate`

the original defect: the plan read never asks the engine, so a missing export reaches the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V1_no_preflight_before_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if planned.items:
        try:
```

New text:

```
    if False:
        try:
```

### `r677.V2_preflight_on_a_plan_of_nothing`

an empty staging folder is refused over the export instead of shown as a plan of nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V2_preflight_on_a_plan_of_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if planned.items:
        try:
```

New text:

```
    if True:
        try:
```

### `r677.V3_refusal_never_replaces_the_gate`

the preflight refusal is caught and dropped, so the gate is offered over an unusable export

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V3_refusal_never_replaces_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`

Old text:

```
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
            raise unusable from None
```

New text:

```
        if False:
            raise unusable from None
```

### `r677.V5_preflight_raises_directly`

the preflight refusal is raised at once, so a recorded abort over a missing export refuses instead of ending in nothing done

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V5_preflight_raises_directly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        except CratekitError as exc:
            unusable = exc
```

New text:

```
        except CratekitError as exc:
            raise exc
```

### `r677.V6_manifest_rows_not_handed_over`

the plan read asks the export check without the manifest's label rows, so a label layout the export cannot take reaches the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V6_manifest_rows_not_handed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`

Old text:

```
                label_rows=manifest.rows if manifest is not None else (),
```

New text:

```
                label_rows=(),
```

### `r770-b.B1_landing_never_takes_the_native_path`

intake_land: ignore the switch, so a native intake tree is landed through the bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `r770-b.json`, row `B1_landing_never_takes_the_native_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 28 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id-KeyID]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    if medium.native:
```

New text:

```
    if False:
```

### `u110-b.B1_pass_names_file`

--pass no longer names the intake file, so sync mark cannot find the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B1_pass_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_gets_a_distinct_name_and_one_pass_is_never_merged`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`

Old text:

```
    if pass_name is not None:
        return pass_name
    if name
```

New text:

```
    if name
```

### `u110-b.B2_name_names_file`

--name alone no longer names the intake file, breaking a landing typed the old way

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B2_name_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`
- Collected: 81 against a baseline of 81
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    if name is not None:
        return name
    return default_name
```

New text:

```
    return default_name
```

### `u110-b.B3_check_pass`

A --pass holding a slash or nothing is not refused before the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B3_check_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[ padded]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[a/b]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[a\\b]`

Old text:

```
    _check_pass(pass_name)

```

New text:

```
(empty)
```

### `u110-b.B4_recheck_xml`

The xml landing does not ask again under the lock whether its default name is still free

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B4_recheck_xml`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_default_name_taken_after_the_gate_is_refused_under_the_lock`

Old text:

```
            _still_free(cfg, batch)

```

New text:

```
            pass

```

### `u110-b.B5_recheck_native`

The native landing does not ask again under the lock whether its default name is still free

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B5_recheck_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing`

Old text:

```
                _still_free(cfg, planned.batch)

```

New text:

```
                pass

```

### `u110-b.B6_intake_lock`

The landing takes only the batch lock and not the intake file's

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B6_intake_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`

Old text:

```
    with landing.batch_lock(batch), landing.intake_lock(stem):
```

New text:

```
    with landing.batch_lock(batch):
```

### `u110-b.B7_name_overrides`

--name is ignored and the default name is always taken

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B7_name_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 125 against a baseline of 125
- Kills: 27 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        ctx.args.name
        if ctx.args.name is not None
        else batch_name.readable(
```

New text:

```
        batch_name.readable(
```

### `u110-b.B8_shown_playlist`

The xml gate screen no longer names the batch playlist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B8_shown_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`

Old text:

```
        "playlist": planned.batch,

```

New text:

```
(empty)
```

### `u113-b.B7_digest_blind_to_split`

The xml gate's digest does not cover the split, so an answer given for one carries out another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u113-b.json`, row `B7_digest_blind_to_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_answer_given_for_one_split_is_stale_for_another`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`

Old text:

```
        identity["playlists"] = [claimed.identity() for claimed in split]
```

New text:

```
        pass
```

### `u113-b.B8_pending_names_unheld`

Names an intake file still waiting on its import holds are not held

- File: `src/cratekit/intake/land_cli.py`
- Source: `u113-b.json`, row `B8_pending_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
    taken = (*(held if isinstance(held, tuple) else ()), *account_playlists.pending_names(cfg))
```

New text:

```
    taken = held if isinstance(held, tuple) else ()
```

### `u120.C2_hearts_not_claimed`

intake_land: no file is a heart

- File: `src/cratekit/intake/land_cli.py`
- Source: `u120.json`, row `C2_hearts_not_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    hearted = account_playlists.hearted(cfg, pass_name, planned.items)
```

New text:

```
    hearted = ()
```

### `u127.L6_bridge_ignores_calibration`

The bridge names the vocals verb as owed on an uncalibrated library

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L6_bridge_ignores_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if cut is None:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

New text:

```
    if False:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

### `u128-b.B3_owned_unresolved_at_gate`

The bridge verb does not find the owned tracks in the export before the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128-b.json`, row `B3_owned_unresolved_at_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`

Old text:

```
    split, emptied = landing.owned_in_export(cfg, split, export)
```

New text:

```
    emptied = ()
```

### `u128.L1_bridge_warning_unsaid`

The bridge landing does not put the left rows on its warnings

- File: `src/cratekit/intake/land_cli.py`
- Source: `u128.json`, row `L1_bridge_warning_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`

Old text:

```
            *account_playlists.left_warning((*emptied, *landed.left)),
```

New text:

```
            *account_playlists.left_warning(()),
```

### `u146-c.L2_empty_landing_no_op`

_land_native: an empty landing ends NO_OP as before, its owned hearts never placed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L2_empty_landing_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if owned:
            return _place_owned(
```

New text:

```
        if owned and False:
            return _place_owned(
```

### `u156.L23_label_beside_manifest`

_label_flag: accept --label beside --manifest, so one of two answers silently wins

- File: `src/cratekit/intake/land_cli.py`
- Source: `u156.json`, row `L23_label_beside_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_blank_label_or_two_label_sources_are_refused_before_the_gate`

Old text:

```
    if manifest is not None:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest
```

New text:

```
    if False:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest
```

### `u156.L24_label_on_the_bridge`

_label_flag: accept --label on the bridge, where the landing files nothing from it

- File: `src/cratekit/intake/land_cli.py`
- Source: `u156.json`, row `L24_label_on_the_bridge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_label_flag_on_the_bridge_is_refused_before_the_gate_naming_it[--label-from-tags]`
  - `tests/test_intake_land_labels_native.py::test_a_label_flag_on_the_bridge_is_refused_before_the_gate_naming_it[--label]`

Old text:

```
    if not medium.native:
        raise refuse(
            "intake-list-unusable",
            f"{flag} files the batch
```

New text:

```
    if False:
        raise refuse(
            "intake-list-unusable",
            f"{flag} files the batch
```

### `u162.L10_interrupt_cancel`

_rehearse_native: an interrupt reported as internal-error rather than cancelled

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L10_interrupt_cancel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure1-cancelled]`

Old text:

```
            "cancelled",
```

New text:

```
            "internal-error",
```

### `u162.L12_rehearsal_equal`

rehearsal_facts: report every rehearsal as equal to the live plan

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L12_rehearsal_equal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`

Old text:

```
    equal = found.get("digest") == digest
```

New text:

```
    equal = True
```

### `u162.L1_bridge_refusal`

intake_land: drop the refusal of --rehearse on an intake tree on the xml bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L1_bridge_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`

Old text:

```
    if rehearse and not medium.native:
```

New text:

```
    if False:
```

### `u162.L2_area_plan_compare`

_rehearse_in: drop the refusal of an area plan that is not the live plan, so a differing plan is applied

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L2_area_plan_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
        if differ:
            raise refuse(
```

New text:

```
        if False:
            raise refuse(
```

### `u162.L4_occupied_hold`

_rehearse_in: drop the hold of the live batch folder's names at the area (round one's fix)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L4_occupied_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`

Old text:

```
            if (target / item.name).exists() or (target / item.name).is_symlink():
```

New text:

```
            if False:
```

### `u162.L6_gridless_read_back`

_rehearse_in: drop the gridless read back of the landed rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L6_gridless_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`

Old text:

```
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after
```

New text:

```
            native.assert_rows_identified(landed.collection)
            rows_after
```

### `u162.L7_identified_read_back`

_rehearse_in: drop the file id read back of the landed rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L7_identified_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`

Old text:

```
            native.assert_rows_gridless(landed.collection)
            native.assert_rows_identified(landed.collection)
            rows_after
```

New text:

```
            native.assert_rows_gridless(landed.collection)
            rows_after
```

### `u162.L8_success_witness`

_rehearse_native: drop the witness on the success path, so a rehearsal that touched the live library reports clean

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L8_success_witness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`

Old text:

```
    rehearsal.assert_untouched(before, kept=area.paths)
    rehearsal.remove(area)
```

New text:

```
    rehearsal.remove(area)
```

### `u162.L9_kept_area_named`

_rehearse_native: a refusal inside the rehearsal no longer carries the kept area in its detail

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L9_kept_area_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[None-backup-acknowledgment]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure0-internal-error]`
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
            detail={**dict(inner.detail), "rehearsal_area": [str(path) for path in area.paths]},
```

New text:

```
            detail=dict(inner.detail),
```

### `u164.H1_watch_recorded`

_filed_watch: watch today's year folder alone, never the recorded folder

- File: `src/cratekit/intake/land_cli.py`
- Source: `u164.json`, row `H1_watch_recorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`

Old text:

```
        watched.extend((Path(again).parent, Path(again)))
```

New text:

```
        pass
```

### `u164.H2_scratch_folder`

_rehearse_in: map the scratch plan back from the live folder instead of its own

- File: `src/cratekit/intake/land_cli.py`
- Source: `u164.json`, row `H2_scratch_folder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[the check]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[None-backup-acknowledgment]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure0-internal-error]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure1-cancelled]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        scratch_target = _folder(scratch_rows)
```

New text:

```
        scratch_target = landing.target_dir(area.cfg, planned.batch)
```

### `u165.L3_filing_tail`

_land_native: never file after the landing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L3_filing_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
    if predicted is not None:
        # THE FILING
```

New text:

```
    if False:
        # THE FILING
```

### `u177.C3_flag_beside_label`

_label_flag: drop the refusal of --label-from-tags beside --label, so one label for every file silently wins

- File: `src/cratekit/intake/land_cli.py`
- Source: `u177.json`, row `C3_flag_beside_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_blank_label_or_two_label_sources_are_refused_before_the_gate`

Old text:

```
    if from_tags and given is not None:
        raise refuse(

```

New text:

```
    if False:
        raise refuse(

```

### `u188.M10_detail_mapped_dropped`

_rehearse_in: carry no mapped pairs in the refusal's detail

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M10_detail_mapped_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
                detail={"differs": differ, "mapped": [list(pair) for pair in pairs]},
```

New text:

```
                detail={"differs": differ},
```

### `u188.M11_fields_last_part`

_fields_of: name a field by its last part alone, so a vox row's path reads as rows

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M11_fields_last_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
        names.append(path.split(".", 1)[-1])
```

New text:

```
        names.append(path.rsplit(".", 1)[-1])
```

### `u188.M12_fields_keep_indices`

_fields_of: keep the indices, so one field is named once per row

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M12_fields_keep_indices`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
        path = re.sub(r"\[\d+\]", "", line[2:].split(" = ", 1)[0])
```

New text:

```
        path = line[2:].split(" = ", 1)[0]
```

### `u188.M13_fields_repeated`

_fields_of: keep every repeat, so a field ten rows differ in is named ten times

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M13_fields_repeated`
- Moved: the same return of _fields_of, still in land_cli.py; only the function after it changed, since _place_owned moved to land_native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
    return list(dict.fromkeys(names))


def rehearsal_facts(
```

New text:

```
    return names


def rehearsal_facts(
```

### `u188.M1_stored_pair_dropped`

_mapped_back: leave the stored spelling pair out, so FolderPath on a renamed drive is never mapped back (the defect)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M1_stored_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
                (str(scratch_target), str(target)),
                stored,
            )
```

New text:

```
                (str(scratch_target), str(target)),
            )
```

### `u188.M2_scratch_stored_under_the_mount`

_mapped_back: spell the area's folder with no base drive, so the scratch side of the stored pair is the mounted spelling

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M2_scratch_stored_under_the_mount`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
            base_drive=scratch_rows.base_drive,
            current_drive=scratch_rows.current_drive,
```

New text:

```
            base_drive=None,
            current_drive=scratch_rows.current_drive,
```

### `u188.M3_live_stored_under_the_mount`

_mapped_back: spell the live folder with no base drive, so the area's FolderPath maps to the mounted spelling the live rows do not carry

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M3_live_stored_under_the_mount`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
            target, base_drive=rows.base_drive, current_drive=rows.current_drive
```

New text:

```
            target, base_drive=None, current_drive=rows.current_drive
```

### `u188.M4_staging_pair_dropped`

_mapped_back: leave the staging pair out, so every from line keeps the area's staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M4_staging_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[the check]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[None-backup-acknowledgment]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure0-internal-error]`
  - `tests/test_intake_land_rehearse.py::test_a_failed_rehearsal_keeps_its_area_and_names_it[failure1-cancelled]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - ... and 3 more, see the JSON sidecar

Old text:

```
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
```

New text:

```
                (str(scratch_target), str(target)),
```

### `u188.M6_mapped_as_lines`

_rehearse_in: map the area's plan after it is printed, so a JSON escaped accent or quote is never mapped (the review's round one)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M6_mapped_as_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
        back = rehearsal.lines(
            rehearsal.mapped(
                plan_identity(staged, scratch_rows, target=scratch_target, archived=archived),
                pairs,
            )
        )
```

New text:

```
        back = rehearsal.mapped(
            plan_lines(staged, scratch_rows, target=scratch_target, archived=archived), pairs
        )
```

### `u188.M7_signs_swapped`

_rehearse_in: compare live first, so a minus line is the live plan's and the refusal's legend is false

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M7_signs_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_scratch_plan_not_the_live_plan_applies_nothing`
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
        differ = rehearsal.differing(back, lines)
```

New text:

```
        differ = rehearsal.differing(lines, back)
```

### `u188.M8_fields_left_out`

_rehearse_in: name no field in the refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M8_fields_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
f"{len(differ)} line(s), in {', '.join(_fields_of(differ))}, so nothing "
```

New text:

```
f"{len(differ)} line(s), in the plan, so nothing "
```

### `u188.M9_pairs_left_out`

_rehearse_in: state no pair in the refusal, so the spellings compared are not named

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M9_pairs_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_on_a_renamed_drive_a_differing_name_still_refuses`

Old text:

```
                + ", ".join(f"{scratch} to {live}" for scratch, live in pairs)
```

New text:

```
                + "the area's paths"
```

### `u307.R20_land_only_by_default`

land_cli flags table: --land-only stores false, so every landing skips filing unless the flag is given

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R20_land_only_by_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
    ("--land-only", {"action": "store_true"},
```

New text:

```
    ("--land-only", {"action": "store_false"},
```

### `u307.R21_unrunnable_reason_lost`

land_cli._unrunnable: a command line the landing cannot run is refused as internal-error, not intake-list-unusable

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R21_unrunnable_reason_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_rekordbox_running_or_an_export_on_a_native_tree_is_refused_before_the_gate`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`

Old text:

```
        "intake-list-unusable", message, remedy=Remedy.FIX_COMMAND_LINE, steps=steps,
```

New text:

```
        "internal-error", message, remedy=Remedy.FIX_COMMAND_LINE, steps=steps,
```

### `u307.R4_land_cli_getattr_answers_none`

land_cli.__getattr__: answer None for every native medium name read on the verb's module, so ask_then_write, the warning codes and the analysis step read as nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R4_land_cli_getattr_answers_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_writers_native.py`
- Collected: 116 against a baseline of 116
- Kills: 23 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    return getattr(land_native, name)
```

New text:

```
    return None
```

### `u331.S06_landing_room_check_dropped`

intake land: the rehearsal's room check is not called through session before its copy (fixed sample, re-routed from snapshot)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u331.json`, row `S06_landing_room_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`

Old text:

```
    session.assert_room_for_check(area.database)

```

New text:

```
(empty)
```

### `u72-b.M18_refused_unmarked`

The payload marks every planned item landed, refused ones included

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M18_refused_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`

Old text:

```
        entry = refused.get(item["from"])
```

New text:

```
        entry = None
```

### `u72-b.M20_shown_files`

The gate context lists no file names

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M20_shown_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
        "files": [item.name for item in planned.items],
```

New text:

```
        "files": [],
```

### `u72-b.M21_empty_to_engine`

An empty folder goes to the engine, which refuses it

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M21_empty_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if False:
```

### `u72-b.M22_listing_without_isdir`

The empty check lists a folder that may not exist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M22_listing_without_isdir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if folder.is_dir() and not landing.listing(folder):
```

New text:

```
    if not landing.listing(folder):
```

### `u72.M10_default_folder`

The default folder is the library root, not download staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M10_default_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[a file arrived]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
```

New text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.library.root)
```

### `u72.M1_abort_applies`

An abort no longer stops the verb: only an empty plan returns NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M1_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if not planned.items:
```

### `u72.M2_empty_plan_applied`

An empty plan is handed to the engine after the answer instead of returning NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M2_empty_plan_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if option != "apply":
```

### `u72.M3_digest_drops_where`

The digest drops the batch, the target and the intake file, so an answer for one name applies under another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M3_digest_drops_where`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[batch name]`

Old text:

```
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),

```

New text:

```
(empty)
```

### `u72.M4_digest_drops_files`

The digest drops the engine's file fingerprint, so a file arriving after the answer is landed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M4_digest_drops_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[a file arrived]`

Old text:

```
        "files": planned.digest,

```

New text:

```
(empty)
```

### `u72.M5_digest_drops_export`

The digest drops the export path

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M5_digest_drops_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[export]`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        "export": str(export),

```

New text:

```
(empty)
```

### `u72.M6_digest_drops_folder`

The digest drops the folder path, so a twin folder with the same names applies

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M6_digest_drops_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[folder]`

Old text:

```
        "folder": str(planned.folder),
        "batch": planned.batch,
```

New text:

```
        "batch": planned.batch,
```

### `u72.M7_gate_digest_none`

The gate is asked with no digest, so no answer is ever stale

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M7_gate_digest_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 23216 against a baseline of 23216
- Kills: 5 (killed)
- Promoted: subset killed 0, full suite killed 5
- Killed:
  - `tests/test_crate_sync_skill.py::test_step_three_re_planned_on_its_stopped_run_names_the_rehearsal_and_lands`
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_mount_it_is_as_it_was`

Old text:

```
        digest=payload["digest"],
```

New text:

```
        digest=None,
```

### `u72.M9_default_name_colons`

The default batch name keeps the run id's colons

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M9_default_name_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`

Old text:

```
    return run_id.replace(":", "")
```

New text:

```
    return run_id
```

### `u77-c.C6_gate_manifest_bytes`

_payload: leave the manifest's bytes out of the plan identity, so the gate accepts an answer given against other rows (the gate layer alone, the engine's own check left in place)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C6_gate_manifest_bytes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`

Old text:

```
identity["manifest_bytes"] = manifest.digest
```

New text:

```
identity["manifest_bytes"] = ""
```

### `u77-c.C7_digest_handed_to_engine`

intake_land: hand the engine no fingerprint, so a manifest rewritten between the gate and the first move is filed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C7_digest_handed_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`

Old text:

```
manifest_digest=manifest.digest if manifest is not None else None,
```

New text:

```
manifest_digest=None,
```

### `u77-c.C8_unfiled_rows_warned`

intake_land: warn about refused files only, so a label row filed under nothing is named nowhere a person reads

- File: `src/cratekit/intake/land_cli.py`
- Source: `u77-c.json`, row `C8_unfiled_rows_warned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`

Old text:

```
for entry in (*landed.refused, *landed.unlabelled)
```

New text:

```
for entry in (*landed.refused,)
```

### `r770-b.B2_gate_asked_before_the_acknowledgment`

ask_then_write: ask the gate without reading the backup acknowledgment first, on both verbs

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B2_gate_asked_before_the_acknowledgment`
- Moved: the same acknowledgment read before the gate is asked, in the shared ask then write of the native landing, which U307 moved from land_cli.py to land_native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_no_acknowledgment_refuses_before_the_gate`
  - `tests/test_intake_writers_native.py::test_no_acknowledgment_refuses_before_the_gate`

Old text:

```
        session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r770-b.B3_an_abort_writes`

ask_then_write: write whatever the answer was

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B3_an_abort_writes`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_abort_moves_nothing_and_writes_nothing, test_an_abort_writes_nothing, were folded by the trim into test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database, test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database, the abort test's steps and checks, verbatim at the end of each file's gate screen test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        if option != "apply":
```

New text:

```
        if option == "never":
```

### `u120.C1_no_skip_note`

favorites_notes: a skipped placement is not said

- File: `src/cratekit/intake/land_native.py`
- Source: `u120.json`, row `C1_no_skip_note`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
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
    if skipped:
        return [
            {
                "code": FAVORITES_SKIPPED,
```

New text:

```
    if False:
        return [
            {
                "code": FAVORITES_SKIPPED,
```

### `u126.P3_gate_fact`

Rename the content link fact on the gate screen, so the value and its count are not where the person reads them

- File: `src/cratekit/intake/land_native.py`
- Source: `u126.json`, row `P3_gate_fact`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 77 against a baseline of 77
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        "content link": (
```

New text:

```
        "link": (
```

### `u127.L1_screen_line_blind`

The native screen counts no tagged row

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L1_screen_line_blind`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_the_screen_counts_the_tagged_rows_against_the_cut, were folded by the trim into test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut, its check of the vox line counting the tagged rows against the cut, with the rescore across the cut added
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`

Old text:

```
        f"{len(rows.vox_tagged())} of {len(adding)} added row(s), each whose voxlevel "
```

New text:

```
        f"{len(adding)} of {len(adding)} added row(s), each whose voxlevel "
```

### `u127.L2_items_carry_no_vox`

The gate items carry no score and no answer

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L2_items_carry_no_vox`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[below]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[zero]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`

Old text:

```
        if row.action == native.ADD and rows.vox_cut is not None and not rows.vox_blocked:
```

New text:

```
        if False:
```

### `u127.L3_totals_from_writer`

Count the written associations as tagged instead of what adoption reads back

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L3_totals_from_writer`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
    voxed = sum(1 for row in landed.collection.added if row.vox)
```

New text:

```
    voxed = landed.collection.vox_written
```

### `u127.L4_missing_unsaid`

Say nothing when a planned tag does not read back

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L4_missing_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
    if collection.vox_missing:
```

New text:

```
    if False:
```

### `u127.L5_unscored_unsaid`

Say nothing about a file with no score

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L5_unscored_unsaid`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_a_file_with_no_score_gets_no_tag_and_is_named, were folded by the trim into test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named, its check that the screen names the file with no score and tags the scored one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    if not collection.vox_unscored:
```

New text:

```
    if True:
```

### `u127.L7_land_warnings_unsaid`

intake land gives no vox warning

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L7_land_warnings_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`
- Collected: 60 against a baseline of 60
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_unreadable]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    warnings.extend(vox_warnings(landed.collection))
```

New text:

```
    warnings.extend([])
```

### `u128-b.N3_native_owned_not_found`

The native verb asks no candidate row for the owned tracks, so every one is left

- File: `src/cratekit/intake/land_native.py`
- Source: `u128-b.json`, row `N3_native_owned_not_found`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
        cfg, named, native.candidate_rows(db, names)
```

New text:

```
        cfg, named, ()
```

### `u128.L2_native_warning_unsaid`

The native landing does not put the left rows on its warnings

- File: `src/cratekit/intake/land_native.py`
- Source: `u128.json`, row `L2_native_warning_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
    warnings.extend(account_playlists.left_warning(landed.collection.left))
```

New text:

```
    warnings.extend(account_playlists.left_warning(()))
```

### `u146-c.L3_gate_asked_for_nothing`

_place_owned: a pass whose owned hearts are all placed opens the database to write and asks the gate over nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u146-c.json`, row `L3_gate_asked_for_nothing`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op, test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing, test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess, test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill, were folded by the trim into test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded, test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write, the four owned heart cases that ask nothing and end no_op, now read through the files' shared _no_op helper
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_owned_hearts_an_empty_landing_cannot_place_alone_are_no_write`

Old text:

```
    if not first.writes:
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)
```

New text:

```
(empty)
```

### `u146-c.L4_missing_source_refuses`

_place_owned: a library with no All Favorites refuses the empty landing instead of ending NO_OP and saying why

- File: `src/cratekit/intake/land_native.py`
- Source: `u146-c.json`, row `L4_missing_source_refuses`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return ctx.envelope(
            data=empty,
```

New text:

```
        raise
        return ctx.envelope(
            data=empty,
```

### `u153.L1_facts_colour_count`

land_cli favorites_facts: count only the items, so the owned hearts are left out of the Pink total shown

- File: `src/cratekit/intake/land_native.py`
- Source: `u153.json`, row `L1_facts_colour_count`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit, were folded by the trim into test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one, its check that both hearts take Pink in the one commit, with the count on the screen
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
        facts["rows to colour Pink"] = len(plan.items) + len(plan.colour)
```

New text:

```
        facts["rows to colour Pink"] = len(plan.items)
```

### `u153.L3_notes_colour_skipped`

land_cli favorites_notes: never emit the missing-Pink note, so a landing that coloured nothing says nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u153.json`, row `L3_notes_colour_skipped`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_with_no_pink_row_the_landing_places_the_heart_and_warns, were folded by the trim into test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made, the no Pink row case, which still places the hearts, leaves them uncoloured and warns with the same code
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`

Old text:

```
    if placed.colour_skipped:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

New text:

```
    if False:
        notes.append(
            {
                "code": colour_mod.PINK_COLOUR_MISSING,
```

### `u157.L1_selection_counts`

awaiting_analysis: count no row as carrying dyn

- File: `src/cratekit/intake/land_native.py`
- Source: `u157.json`, row `L1_selection_counts`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_the_warning_names_both_selections_and_counts_each, were folded by the trim into test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection, the warning naming both selections and counting each, now over two rows
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landing_whose_every_row_is_dyn_says_the_visit_ends_on_dynamic`
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
    dyned = sum(1 for row in collection.added if row.dyn)
    normal
```

New text:

```
    dyned = 0
    normal
```

### `u157.L2_blocked_unnamed`

dyn_warnings: a blocked landing names none of its variable rows

- File: `src/cratekit/intake/land_native.py`
- Source: `u157.json`, row `L2_blocked_unnamed`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    if collection.dyn_blocked:
        untagged.update(collection.dyn_variable)

```

New text:

```
(empty)
```

### `u161.L1_landing_pins_nothing`

ask_then_write: pin nothing, so every native write's answer is free of the file again

- File: `src/cratekit/intake/land_native.py`
- Source: `u161.json`, row `L1_landing_pins_nothing`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another, were folded by the trim into test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path, the continuation over another file refused stale, each screen naming the file it reads and writes
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
            spec, plan=data, context=shown(rows), pinned={DATABASE_PIN: str(opened)}
```

New text:

```
            spec, plan=data, context=shown(rows), pinned={}
```

### `u161.P6_screen_drops_path`

collection_facts: show the root's name where the database path was, so the screen no longer says which file is written

- File: `src/cratekit/intake/land_native.py`
- Source: `u161.json`, row `P6_screen_drops_path`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "reads and writes": str(rows.database),
```

New text:

```
        "reads and writes": str(rows.root_name),
```

### `u165.L1_bridge_skip`

_land_native: predict a filing on a routing tree still on the bridge

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L1_bridge_skip`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`
- Collected: 54 against a baseline of 54
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if medium.files_natively
```

New text:

```
            if True
```

### `u165.L2_land_only`

planner: predict and file under --land-only too

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L2_land_only`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`
- Collected: 54 against a baseline of 54
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`
  - `tests/test_intake_land_filing.py::test_a_routing_tree_on_the_bridge_files_nothing_and_the_screen_names_it`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`

Old text:

```
            if unfiled:
                return made
```

New text:

```
            if False:
                return made
```

### `u165.L4_files_into`

_native_payload: drop each item's files into

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L4_files_into`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
        if str(row.target) in sorted_into:
```

New text:

```
        if False:
```

### `u166.A11_warning_names_batch`

awaiting_analysis: name the batch playlist again instead of Analyze

- File: `src/cratekit/intake/land_native.py`
- Source: `u166.json`, row `A11_warning_names_batch`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_writers_native.py`
- Collected: 63 against a baseline of 63
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
                f"{collection.analyze_name} playlist, which holds every row waiting "
```

New text:

```
                f"{collection.playlist} playlist, which holds every row waiting "
```

### `u177.C4_flag_ignored`

label_plan: ignore --label-from-tags, so the batch lands filed under nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u177.json`, row `C4_flag_ignored`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_label_source_moves_the_digest_and_an_answer_for_one_is_stale_for_another`

Old text:

```
            if label_from_tags:
                return label_filing.plan_for_tags(db, medium, files=files)

```

New text:

```
            if False:
                return label_filing.plan_for_tags(db, medium, files=files)

```

### `u181.L1_half_is_a_warning`

land_cli vox_plan_warnings: warn at exactly half the added rows unscored

- File: `src/cratekit/intake/land_native.py`
- Source: `u181.json`, row `L1_half_is_a_warning`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_half_a_batch_unscored_is_said_on_the_line_and_is_no_warning, were folded by the trim into test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen, the bound of more than half unscored, where one in two is the line's alone, beside the warning case
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen`

Old text:

```
    if not adding or 2 * len(unscored) <= len(adding):
```

New text:

```
    if not adding or 2 * len(unscored) < len(adding):
```

### `u181.L2_coefficient`

land_cli vox_plan_warnings: halve the coefficient, so only an unscored batch above the whole warns

- File: `src/cratekit/intake/land_native.py`
- Source: `u181.json`, row `L2_coefficient`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_batch_mostly_unscored_carries_a_warning_with_its_code_on_the_gate_screen`

Old text:

```
    if not adding or 2 * len(unscored) <= len(adding):
```

New text:

```
    if not adding or 1 * len(unscored) <= len(adding):
```

### `u307.R22_colour_notes_drop_held`

land_native._colour_notes: leave out the note naming the rows that keep a colour a person chose

- File: `src/cratekit/intake/land_native.py`
- Source: `u307.json`, row `R22_colour_notes_drop_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`

Old text:

```
    if placed.held:
```

New text:

```
    if False:
```

### `u319.M8_ok_on_any_field`

land_cli: the short path's OK offered whatever the dialog shows

- File: `src/cratekit/intake/land_native.py`
- Source: `u319.json`, row `M8_ok_on_any_field`
- Moved: the same line of the short path's visit wording, which U307 moved from land_cli.py to land_native.py with the native landing
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_the_auto_analysis_step_cancels_on_any_other_field_and_leaves_dyn_to_dynamic`
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    "on its Auto Analysis dialog only when it shows every one of those Normal "
```

New text:

```
    "on its Auto Analysis dialog whatever it shows of those Normal "
```

### `u319.M9_warning_drops_the_short_path`

land_cli: the awaiting analysis warning names one path again

- File: `src/cratekit/intake/land_native.py`
- Source: `u319.json`, row `M9_warning_drops_the_short_path`
- Moved: the text moved whole from intake/land_cli.py to intake/land_native.py with its function (U307); the tests that killed it, test_the_warning_names_both_selections_and_counts_each, were folded by the trim into test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection, the warning naming both selections and counting each, now over two rows
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landing_whose_every_row_is_dyn_says_the_visit_ends_on_dynamic`
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
                f"for analysis, and {selections}; {AUTO_ANALYSIS_STEP}; then "
```

New text:

```
                f"for analysis, and {selections}; then "
```

### `u954.M1_no_dyn_case`

awaiting_analysis: never take the no dyn branch, so a landing with no dyn row is told a Dynamic run first on 0 rows and a Normal run last

- File: `src/cratekit/intake/land_native.py`
- Source: `u954.json`, row `M1_no_dyn_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_file_with_no_drift_reading_or_no_number_is_counted_unscored_and_untagged[None-None]`
  - `tests/test_intake_land_dyn_native.py::test_a_file_with_no_drift_reading_or_no_number_is_counted_unscored_and_untagged[lots-variable]`
  - `tests/test_intake_land_dyn_native.py::test_a_tag_written_under_a_removed_value_is_said_and_never_counted`

Old text:

```
    normal = len(collection.added) - dyned
    if not dyned:
```

New text:

```
    normal = len(collection.added) - dyned
    if False:
```

### `u954.M2_every_row_dyn_case`

awaiting_analysis: never take the every row dyn branch, so a batch of only dyn rows is told a Normal run last on 0 rows that leaves the mode Normal (round one's blocking finding)

- File: `src/cratekit/intake/land_native.py`
- Source: `u954.json`, row `M2_every_row_dyn_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landing_whose_every_row_is_dyn_says_the_visit_ends_on_dynamic`

Old text:

```
    elif not normal:
```

New text:

```
    elif False:
```

### `u954.M3_mixed_order`

awaiting_analysis: the mixed batch told Normal first and Dynamic last, the order that leaves the mode on Dynamic

- File: `src/cratekit/intake/land_native.py`
- Source: `u954.json`, row `M3_mixed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
            f"run Analyze Tracks first on the {dyned} row(s) carrying the dyn My Tag "
            f"with {drift.DYNAMIC_SETTINGS} as the Normal run's, then last on the "
```

New text:

```
            f"run Analyze Tracks last on the {dyned} row(s) carrying the dyn My Tag "
            f"with {drift.DYNAMIC_SETTINGS} as the Normal run's, then first on the "
```

### `u954.M5_auto_step_condition_landing`

AUTO_ANALYSIS_STEP in land_native: the closing Normal run told whatever the rows, with no dyn row or no row without it

- File: `src/cratekit/intake/land_native.py`
- Source: `u954.json`, row `M5_auto_step_condition_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_the_auto_analysis_step_cancels_on_any_other_field_and_leaves_dyn_to_dynamic`
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    f"{drift.DYNAMIC_SETTINGS}, and then, when they did and a row lacks the tag, one "
```

New text:

```
    f"{drift.DYNAMIC_SETTINGS}, and then, whatever the rows carry, always one "
```

### `u954.M7_untagged_rows_order`

dyn_warnings: the untagged variable rows told to run Dynamic after the Normal run, which leaves the mode on Dynamic

- File: `src/cratekit/intake/land_native.py`
- Source: `u954.json`, row `M7_untagged_rows_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
            f"{drift.DYNAMIC_SETTINGS}, before any Normal run and left out of it, "
```

New text:

```
            f"{drift.DYNAMIC_SETTINGS}, after the Normal run and left out of it, "
```

### `r432-a.A1_key_casefold`

lock_key: drop the casefold, so two spellings of one folder on a case insensitive volume each get their own lock

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A1_key_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`

Old text:

```
    folded = unicodedata.normalize("NFC", batch.casefold())
```

New text:

```
    folded = unicodedata.normalize("NFC", batch)
```

### `r432-a.A3_lock_never_taken`

batch_lock: hand back the lock's path without taking it, so nothing is excluded

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A3_lock_never_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`

Old text:

```
        path = lock.__enter__()
```

New text:

```
        path = jobs.lock_path(key, root=root)
```

### `r432-a.A5_not_retryable`

batch_lock: mark the held refusal as not retryable, though the holder ending is exactly what a retry waits for

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A5_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`

Old text:

```
            retryable=True,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
```

New text:

```
            retryable=False,
            origin=_ORIGIN,
            detail={"batch": batch, "lock": str(held), "holder": who},
```

### `r432-a.A8_holder_left_out`

batch_lock: leave the holder out of the message, so a person is told a landing is running and not which

- File: `src/cratekit/intake/landing.py`
- Source: `r432-a.json`, row `A8_holder_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`

Old text:

```
            f"another landing under the batch name {batch!r} is running ({who}), "
```

New text:

```
            f"another landing under the batch name {batch!r} is running, "
```

### `r432-b.A4c_lock_outlives_its_with`

What the release tests do hold: drop the release AND keep the lock object alive, which is what a leaked lock is once the collector cannot free it

- File: `src/cratekit/intake/landing.py`
- Source: `r432-b.json`, row `A4c_lock_outlives_its_with`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`

Old text:

```
        lock.__exit__(None, None, None)
```

New text:

```
        globals().setdefault("_LEAKED", []).append(lock)
```

### `r677.E1_export_asked_before_the_library`

the preflight asks the export before the library, so an unmounted volume is named as a missing export

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E1_export_asked_before_the_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`
- Collected: 61 against a baseline of 61
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    _check_batch(plan.batch)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
```

New text:

```
    _check_batch(plan.batch)
    _check_export(export, destination, tree_registry.read(cfg), label_rows)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
```

### `r677.E2_library_check_dropped`

the preflight never asks the library

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E2_library_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`

Old text:

```
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
    if destination.exists():
```

New text:

```
    if destination.exists():
```

### `r677.E3_intake_file_check_dropped`

the preflight never asks whether the intake file is already there

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E3_intake_file_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`

Old text:

```
    if destination.exists():
        raise refuse(
            "output-exists",
```

New text:

```
    if False:
        raise refuse(
            "output-exists",
```

### `r746-b.N8_unsupported_file_moved_anyway`

apply_native: a file the database has no type for is not refused per file and moves

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N8_unsupported_file_moved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`

Old text:

```
        if row.action == native.UNSUPPORTED
    }
```

New text:

```
        if False
    }
```

### `r746-b.N9_placement_check_dropped_from_the_screen`

_screen: a file whose tags resolve to no sub is moved on both media

- File: `src/cratekit/intake/landing.py`
- Source: `r746-b.json`, row `N9_placement_check_dropped_from_the_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`

Old text:

```
            named.get(item) or _unplaceable(item, declared) or _occupied(item, target / item.name)
```

New text:

```
            named.get(item) or _occupied(item, target / item.name)
```

### `r770-c.C3_failure_past_the_gate_loses_its_reason`

write: report every failure past the gate as internal-error, whatever refused

- File: `src/cratekit/intake/landing.py`
- Source: `r770-c.json`, row `C3_failure_past_the_gate_loses_its_reason`
- Moved: the same reason kept for a failure past the gate, now in landing.refuse_past, which U307 made of the copies in file_cli.py and the other landing verbs; file_cli.py calls it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        inner.reason if inner is not None else "internal-error",
```

New text:

```
        "internal-error",
```

### `r770-c.C4_failure_past_the_gate_loses_its_remedy`

write: drop the inner refusal's remedy, so the reason's default answers

- File: `src/cratekit/intake/landing.py`
- Source: `r770-c.json`, row `C4_failure_past_the_gate_loses_its_remedy`
- Moved: the same remedy kept for a failure past the gate, now in landing.refuse_past, which U307 made of the copies in file_cli.py and the other landing verbs; file_cli.py calls it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        remedy=inner.remediation.remedy if inner is not None else None,
```

New text:

```
        remedy=None,
```

### `u110-c.C1_apply_playlist`

The xml landing no longer hands its batch name to the splice, so the playlist is the intake file's stem again

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C1_apply_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_gets_a_distinct_name_and_one_pass_is_never_merged`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`

Old text:

```
            playlist=plan.batch,

```

New text:

```
(empty)
```

### `u110-c.C7_intake_lock_prefix`

The intake lock shares its key with a batch of the same name

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C7_intake_lock_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`
- Collected: 47 against a baseline of 47
- Kills: 13 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`

Old text:

```
lock_key("intake file\0" + stem)
```

New text:

```
lock_key(stem)
```

### `u110-c.C8_plain_dot`

A name starting with a dot passes the plain name rule

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C8_plain_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`

Old text:

```
        and not text.startswith(".")

```

New text:

```
(empty)
```

### `u113-b.B5_export_clash_unasked`

A name the export came to hold since it was chosen is not refused before the moves

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B5_export_clash_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`

Old text:

```
    clash = sorted(set(names) & set(held))
```

New text:

```
    clash: list[str] = []
```

### `u113-b.B6_root_names_unheld`

Names at the export's playlist root, where an import lands first, are not held

- File: `src/cratekit/intake/landing.py`
- Source: `u113-b.json`, row `B6_root_names_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`

Old text:

```
    return (*held, *at_root)
```

New text:

```
    return held
```

### `u113-c.C6_names_checked_after_moves`

The native landing no longer asks whether a chosen name was taken before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u113-c.json`, row `C6_names_checked_after_moves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_name_inbox_came_to_hold_after_the_plan_is_refused_and_nothing_is_written`

Old text:

```
    native.assert_names_still_free(db, rows)
```

New text:

```
    pass
```

### `u128-b.B1_engine_stale_unchecked`

The bridge engine does not read the owned entries again before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B1_engine_stale_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`

Old text:

```
    if now != planned:
```

New text:

```
    if False:
```

### `u128-b.B2_foreign_host_indexed`

Index an export entry whose Location names another machine, which raises out of the index

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B2_foreign_host_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`

Old text:

```
        try:
            locations.location_to_path(recorded)
        except locations.LocationDecodeError:
            continue
        found.append
```

New text:

```
        found.append
```

### `u164.W1_apply_folder`

apply_native: move into the music folder's batch path whatever the plan chose

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W1_apply_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`
- Collected: 50 against a baseline of 50
- Kills: 24 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`
  - `tests/test_intake_land_filed.py::test_a_folder_on_disk_or_one_the_collection_stores_rows_under_is_passed_over`
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_a_name_that_is_a_date_alone_files_as_downloads`
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    target = rows.folder if rows.folder is not None else target_dir(cfg, plan.batch)
```

New text:

```
    target = target_dir(cfg, plan.batch)
```

### `u164.W2_preflight_target`

apply_native: check the library against the music folder rather than the chosen folder

- File: `src/cratekit/intake/landing.py`
- Source: `u164.json`, row `W2_preflight_target`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_filed_folder_on_another_device_is_refused_at_the_move`

Old text:

```
    preflight_native(plan, cfg=cfg, target=target)
```

New text:

```
    preflight_native(plan, cfg=cfg)
```

### `u307.R6_refuse_past_drops_inner_message`

landing.refuse_past: leave the inner failure's own sentence out of the message, so a person reads what was left but not what failed

- File: `src/cratekit/intake/landing.py`
- Source: `u307.json`, row `R6_refuse_past_drops_inner_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 77 against a baseline of 77
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id-KeyID]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`

Old text:

```
        f"{head} ({inner.message if inner is not None else exc}); {tail}",
```

New text:

```
        f"{head}; {tail}",
```

### `u72-b.M23_listing_unfiltered`

The engine's public listing returns every entry, not only audio

- File: `src/cratekit/intake/landing.py`
- Source: `u72-b.json`, row `M23_listing_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_empty_staging_folder_is_a_plan_of_nothing_and_makes_nothing`

Old text:

```
    return _list(folder)


def _digest(
```

New text:

```
    return tuple(folder.iterdir())


def _digest(
```

### `u77-a.A6_no_landed_file_guard`

_file_labels: file a row that resolved to no file this run placed, so a year playlist is written for a track the intake file gave no id

- File: `src/cratekit/intake/landing.py`
- Source: `u77-a.json`, row `A6_no_landed_file_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`

Old text:

```
        if not landed:
            # TRUE OF BOTH ROWS
```

New text:

```
        if landed is None:
            # TRUE OF BOTH ROWS
```

### `r502-a.G5_no_adjudicate`

Skip reading a person's answer back, so a row answered as another track reads as a fresh question and drops out

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G5_no_adjudicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    if asked:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

New text:

```
    if False:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

### `r502-a.G6_no_mount_guard`

Drop the absent music folder refusal before the library walk

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G6_no_mount_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    if not music.is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

New text:

```
    if False:
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

### `r502-a2.G7_frozen_config`

Ask the library at the root the first job froze rather than the current configuration (the review's finding)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a2.json`, row `G7_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`

Old text:

```
    cfg = intake_cli._load()
    music = Path(cfg.library.root) / cfg.library.music_dir
```

New text:

```
    cfg = jobs.frozen_config(origins[0])
    music = Path(cfg.library.root) / cfg.library.music_dir
```

### `r502-b.E2_nothing_written_refusal`

Existing guard sample: drop the refusal for missing tracks none of which could be written

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `E2_nothing_written_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
    if missing and not listed and not in_file:
```

New text:

```
    if False:
```

### `r502-b.G10_since_keys_swapped`

Count a row held since under suppressed_since and a row deleted since under owned_since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G10_since_keys_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
    match.MatchState.MATCHED: "owned_since",
    match.MatchState.SUPPRESSED: "suppressed_since",
```

New text:

```
    match.MatchState.MATCHED: "suppressed_since",
    match.MatchState.SUPPRESSED: "owned_since",
```

### `r502-b.G12_since_check_detail`

Reword the since check so it no longer names the rows in the library since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G12_since_check_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
            f"{since['owned_since']} in the library since, {since['suppressed_since']} "
```

New text:

```
            f"{since['owned_since']} held now, {since['suppressed_since']} "
```

### `r502-b.G9_missing_count_stale`

Report the job's missing count rather than the count still missing now

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G9_missing_count_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        counts["missing"] = len(missing)

```

New text:

```
(empty)
```

### `r502-b2.G13_written_line_for_gained`

Drop the written line's gained branch, so a job whose rows were all gained reads as a job with nothing missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b2.json`, row `G13_written_line_for_gained`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    elif gained:
        said = (
```

New text:

```
    elif False:
        said = (
```

### `r503-a.G10_owned_key`

File an answered row now owned under answered_missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G10_owned_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`
- Collected: 48 against a baseline of 48
- Kills: 30 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_is_no_op_and_writes_nothing`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_a_run_with_nothing_missing_and_nothing_skipped_is_a_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    match.MatchState.MATCHED: "answered_owned",
```

New text:

```
    match.MatchState.MATCHED: "answered_missing",
```

### `r503-a.G1_no_lookup`

Read no answer at all, so every offered row stays offered whatever a person said (R-503 as filed)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G1_no_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    answered = iter(_answered(offered))
```

New text:

```
    answered = iter([False] * len(offered))
```

### `r503-a.G2_found_is_answered`

Treat an item that exists as answered, so an unanswered row is asked again and offered again from the listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G2_found_is_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            said.append(held is not None and held.resolved)
```

New text:

```
            said.append(held is not None)
```

### `r503-a.G4_offered_not_decremented`

Leave an answered row in the offered count, so a rejected row still reads offered 1

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G4_offered_not_decremented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts["offered"] -= 1

```

New text:

```
(empty)
```

### `r503-a.G5_state_not_counted`

Do not count an answered row under the word it resolved to, so an accepted row is not owned

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G5_state_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts[_WORD[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G6_answered_not_counted`

Do not count answered rows under answered_*

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G6_answered_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                now_answered[_ANSWERED[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G7_answered_read_as_since`

Count an answered row as a missing row would be counted, under since, rather than as answered

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G7_answered_read_as_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if report["state"] == "offered":
                # COUNTED
```

New text:

```
            if report["state"] == "never":
                # COUNTED
```

### `r503-a.G8_rejected_not_kept`

Keep only rows the job found missing, so a rejected row is counted and never listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G8_rejected_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if one.state is match.MatchState.MISSING:
                kept.append(n)
```

New text:

```
            if one.state is match.MatchState.MISSING and report["state"] == "missing":
                kept.append(n)
```

### `r503-a.G9_answered_last`

Ask answered rows after missing ones, so a rejected row is listed out of its playlist order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G9_answered_last`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    asking = [
        (job, report)
        for job, report in rows_in
        if report["state"] == "missing" or next(answered)
    ]
```

New text:

```
    asking = sorted(
        [
            (job, report)
            for job, report in rows_in
            if report["state"] == "missing" or next(answered)
        ],
        key=lambda pair: pair[1]["state"] == "offered",
    )
```

### `r503-b.E2_offered_listed`

Existing: list every offered report as missing without asking, the shape the brief forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `E2_offered_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
        if report["state"] == "missing" or next(answered)
```

New text:

```
        if report["state"] == "missing" or next(answered) or True
```

### `r503-b.G11_summary`

Drop the answered_* counts from the summary

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G11_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
        **now_answered,

```

New text:

```
(empty)
```

### `r503-b.G12_answered_check`

Reword the answered check's breakdown

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G12_answered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            f"missing, {now_answered['answered_owned']} in the library, "
```

New text:

```
            f"listed, {now_answered['answered_owned']} owned, "
```

### `r503-b.G13_offered_check`

Reword the offered check's route back to this listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G13_offered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            f"see: crate review list, then list this again",
```

New text:

```
            f"see: crate review list",
```

### `r503-b.G14_no_gone`

Never name the tracks the earlier list holds and this one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G14_no_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    if gone:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G15_no_new`

Never name the tracks this list holds and the earlier one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G15_no_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    if new:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G16_json_uncaught`

Let an earlier file that is not JSON escape the hint as an internal error

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G16_json_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError):
        return []
```

New text:

```
    except (OSError, KeyError, TypeError):
        return []
```

### `r503-b.G17_no_hint`

Drop the hint read from the earlier file altogether

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G17_no_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
        why = _changed_since(out, name, rows)
```

New text:

```
        why = []
```

### `u110-c.C5_missing_hint`

intake missing --run prints --name RUN again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u110-c.json`, row `C5_missing_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
f"--pass {name}, adding
```

New text:

```
f"--name {name}, adding
```

### `u207.I1_missing_never_screens`

intake missing: the askable codes are never screened

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u207.json`, row `I1_missing_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_intake_missing_screens_the_codes_it_will_ask_before_asking_any`

Old text:

```
        found.screen_isrcs(askable)

```

New text:

```
(empty)
```

### `u212.M10_left_out`

missing_cli._listed: drop the staged clause of the left out refusal, so a run with a failed job and every finished row staged refuses

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M10_left_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`

Old text:

```
    if left_out and not listed and not unlisted and not staged_rows:
```

New text:

```
    if left_out and not listed and not unlisted:
```

### `u212.M1_staged_match`

missing_cli._staged: never record a staged row, so a track a staged file carries is listed and downloaded again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M1_staged_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[neither]`

Old text:

```
        if held:
            found.append((n, held[0].path))
```

New text:

```
        if held and False:
            found.append((n, held[0].path))
```

### `u212.M2_own_rows_both`

missing_cli._staged: drop the own rows rule, so a continued pass subtracts its own staged downloads and its list is refused over its earlier copy

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M2_own_rows_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
            continue
```

New text:

```
        if False:
            continue
```

### `u212.M3_own_rows_by_id`

missing_cli._staged: the own rows rule by ISRC alone, the provider id half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M3_own_rows_by_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-provider-id]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if token in isrcs:
```

### `u212.M4_own_rows_by_isrc`

missing_cli._staged: the own rows rule by provider id alone, the ISRC half removed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M4_own_rows_by_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_each_half_of_the_own_rows_rule_keeps_a_row_alone[by-isrc]`

Old text:

```
        if (ref and ref in ids) or token in isrcs:
```

New text:

```
        if ref and ref in ids:
```

### `u212.M5_unread_is_empty`

missing_cli._staged: an unreadable staging folder read as one holding nothing, so the staged row says nothing failed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M5_unread_is_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        return _Staged(folder, unread=str(exc.strerror or exc))
```

New text:

```
        return _Staged(folder)
```

### `u212.M6_absent_folder`

missing_cli._staged: drop the absent folder guard, so a machine with no staging folder yet reports the folder unreadable

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M6_absent_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        if not folder.exists():
```

New text:

```
        if False:
```

### `u212.M7_outcome_staged`

missing_cli._listed: every row staged answers no_op, so a pass ends before the landing that takes them

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M7_outcome_staged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
        outcome=Outcome.OK if listed or unlisted or staged_rows else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed or unlisted else Outcome.NO_OP,
```

### `u212.M8_summary_count`

missing_cli._listed: the summary's staged count read as zero, the number the pass reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M8_summary_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_run_with_a_failed_job_and_every_finished_row_staged_answers_ok`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[204.flac]`
  - `tests/test_intake_missing_staged.py::test_a_staged_file_counts_under_its_provider_name_or_its_given_name[Lumen Drift - Salt Road.flac]`

Old text:

```
        "staged": len(staged_rows),
```

New text:

```
        "staged": 0,
```

### `u212.M9_unread_status`

missing_cli._staged_check: an unreadable staging folder said on an info row rather than a failing one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u212.json`, row `M9_unread_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_staged.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_staged.py::test_a_staged_file_carrying_a_wanted_tracks_isrc_is_named_staged_and_not_listed`

Old text:

```
            "staged",
            "fail",
```

New text:

```
            "staged",
            "info",
```

### `u307.R12_summary_head_written_zero`

missing_cli._summary_head: report written as zero, so the summary says nothing was listed when rows were written

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u307.json`, row `R12_summary_head_written_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`
- Collected: 107 against a baseline of 107
- Kills: 23 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_an_isrc_is_folded_before_it_is_asked_and_a_malformed_one_is_never_asked`
  - `tests/test_intake_missing_isrc.py::test_the_same_id_twice_in_one_answer_is_one_id_and_is_listed`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    head.update(written=len(written.listed))
```

New text:

```
    head.update(written=0)
```

### `u307.R13_named_by_isrc_resolves_unasked`

missing_cli._named_by_isrc: resolve the catalogue even when no row carries an askable ISRC, so a job with none spends a login

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u307.json`, row `R13_named_by_isrc_resolves_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`
- Collected: 48 against a baseline of 48
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`
  - `tests/test_intake_missing_isrc.py::test_a_set_with_no_isrc_resolves_no_catalogue_and_spends_no_login`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
    if askable:
        found = (resolve or _catalogue_once())()
```

New text:

```
    if True:
        found = (resolve or _catalogue_once())()
```

### `u69-b.M10_out_not_a_folder`

Drop the refusal of an --out that exists and is not a folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M10_out_not_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    if out.exists() and not out.is_dir():
```

New text:

```
    if False:
```

### `u69-b.M12_unlisted_status`

Report unlisted missing tracks as a note instead of a failing check

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M12_unlisted_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
"fail" if unlisted else "ok",
```

New text:

```
"info" if unlisted else "ok",
```

### `u69-b.M16_next_command`

Drop the literal next command from the written check a person reads

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M16_next_command`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
written to {written.list_path}; next: {command}"
```

New text:

```
written to {written.list_path}"
```

### `u69-b.M17_lists_folder`

Write into download staging itself rather than its lists folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M17_lists_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
out = intake_cli._load().paths.download_staging / LISTS_DIR
```

New text:

```
out = intake_cli._load().paths.download_staging
```

### `u69-b.M18_inner_cause`

Drop the failed job's own cause from the refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M18_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`

Old text:

```
            inner=job.cause,
```

New text:

```
            inner=None,
```

### `u69-b.M19_resume_step`

Drop the resume command from an open job's refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M19_resume_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
            f"finish it with: crate {argv}" if job.is_open() else
```

New text:

```
            "finish it first" if job.is_open() else
```

### `u69.M1_handler_key`

Drop the refusal of a job queued under another verb's handler key

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M1_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_is_refused`

Old text:

```
    if job.handler_key not in intake_cli.INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u69.M2_succeeded_only`

Drop the refusal of a job that is not succeeded (open, failed, cancelled)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M2_succeeded_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u69.M4_report_coverage`

Drop the refusal when the reports do not cover the items one for one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M4_report_coverage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if False:
```

### `u69.M5_by_count`

Compare reports to items by count instead of by identifier

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M5_by_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if len(reported) != len(wanted):
```

### `u69.M6_state_word`

Drop the refusal of a report whose state word this verb cannot read

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M6_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
```

New text:

```
        if not isinstance(report.get("track"), Mapping):
```

### `u73-b.B2_every_ref_kept`

Stop accumulating every reference an id came from

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B2_every_ref_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
            refs.append(said)
```

New text:

```
            pass
```

### `u73-b.B3_first_source_wins`

Let the last job an id came from win its provenance instead of the first

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B3_first_source_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        first.setdefault(ref, job)
```

New text:

```
        first[ref] = job
```

### `u73.A10_every_job_skipped`

Drop the refusal of a run whose every job failed, left to the layer after it

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A10_every_job_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u73.A1_blank_run`

Drop the refusal of a blank --run, so a blank run is compared as it stands

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A1_blank_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run`

Old text:

```
    if not run_id.strip():
```

New text:

```
    if False:
```

### `u73.A2_library_filter`

Drop the library half of the run selection, so the run alone picks jobs

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A2_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
and job.library_id == library_id
```

New text:

```
and True
```

### `u73.A3_run_filter`

Drop the run half of the selection, so every intake job for the library is listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A3_run_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
(job.payload or {}).get(RUN_ID) == run_id
```

New text:

```
True
```

### `u73.A4_intake_key_filter`

Drop the intake handler key filter, so a labels or favourites job in the run is selected

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A4_intake_key_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
```

New text:

```
            if True
```

### `u73.A5_oldest_first`

Reverse the job order, newest first, so first source wins picks the later playlist

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A5_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
key=lambda job: (job.created, job.job_id),
```

New text:

```
key=lambda job: (job.created, job.job_id), reverse=True,
```

### `u73.A7_open_refuses`

Drop the refusal of a run holding an open job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A7_open_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
    if still_open:
```

New text:

```
    if False:
```

### `u73.A8_failed_refuses`

Drop the refusal of a run holding a failed or cancelled job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A8_failed_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if False:
```

### `u73.A9_skip_failed_ignored`

Ignore --skip-failed, so a failed job refuses the run whatever the flag says

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A9_skip_failed_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if unfinished:
```

### `u78-a.A3_several_listed`

An ISRC filed under several tracks lists the first, the guess R-356 forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A3_several_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_intake_missing_isrc.py::test_the_order_the_provider_answers_in_does_not_change_the_files`

Old text:

```
        elif len(answer) == 1:
```

New text:

```
        elif len(answer) >= 1:
```

### `u78-a.A5_outage_read_as_none`

A provider that could not answer is read as filing no track, so the row is handed on and the verb writes

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A5_outage_read_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`

Old text:

```
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                raise refuse(
```

New text:

```
            except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
                answers[code] = ()
                continue
                raise refuse(
```

### `u78-a.A6_blank_id_dropped`

A track with no identifier in the answer is dropped, so one named and one unnamed reads as one id

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-a.json`, row `A6_blank_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_the_same_id_twice_in_one_answer_is_one_id_and_is_listed`

Old text:

```
    if any(not one for one in ids):
```

New text:

```
    ids = [one for one in ids if one]
    if False:
```

### `u78-b.B1_unwritable_refuses_whole`

The per row text line check before writing is removed, so one unwritable row refuses the verb again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-b.json`, row `B1_unwritable_refuses_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
            try:
                listdoc.text_line(row)
            except listdoc.ListDocRefused:
```

New text:

```
            try:
                pass
            except listdoc.ListDocRefused:
```

### `u78-b.B3_ids_unsorted`

The identifiers in a several reason are written in provider order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-b.json`, row `B3_ids_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_the_order_the_provider_answers_in_does_not_change_the_files`

Old text:

```
f"({', '.join(sorted(answer))}), and which release to download is "
```

New text:

```
f"({', '.join(answer)}), and which release to download is "
```

### `u78-d.A4_cratekit_error_passthrough_again`

A product refusal raised by the catalogue is relabelled unavailable-transient

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u78-d.json`, row `A4_cratekit_error_passthrough_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_isrc.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`

Old text:

```
            except CratekitError:
                raise
            except Exception as exc:
```

New text:

```
            except Exception as exc:
```

### `u79-c.C2_owned_row_searched`

A row the library holds is counted missing and searched for

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C2_owned_row_searched`
- Moved: Anchored where u325-replay-after.json replayed it: Same loop in _missing_for_list; U298 replaced its three state branches with a lookup in match_cli.SETTLED_WORDS, whose MATCHED entry is owned, so excluding owned sends a matched row to the missing branch, which is what disabling the MATCHED branch did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_list_the_library_holds_entirely_is_a_no_op_that_spends_no_login`
  - `tests/test_intake_missing_search.py::test_an_owned_row_is_never_searched_for`

Old text:

```
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None:
            counts[word] += 1
```

New text:

```
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None and word != "owned":
            counts[word] += 1
```

### `u79-c.C3_accepted_held_listed_again`

An accepted candidate the library now holds is listed for download again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C3_accepted_held_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`

Old text:

```
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n]
```

New text:

```
            if False:
                proposals[n]
```

### `u79-c.C4_nothing_found_is_a_no_op`

Missing rows with no route to any of them end as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C4_nothing_found_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if unfound and not listed and not asked:
```

New text:

```
    if False:
```

### `u79-c.C5_foreign_ref_names_a_row`

Another service's identifier is read as the provider's, and the row is in no file

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C5_foreign_ref_names_a_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_missing_row_of_another_services_list_is_searched_for_and_not_dropped`
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
    return str(wanted.ref or "").strip() if wanted.origin == match.TIDAL else ""
```

New text:

```
    return str(wanted.ref or "").strip()
```

### `u79-c.C6_isrc_named_keeps_origin`

A foreign row named by ISRC keeps its origin, so the emitter takes the ref off again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C6_isrc_named_keeps_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_rows_asked_by_isrc_and_rows_searched_for_share_one_catalogue`

Old text:

```
                named.append(replace(one, ref=answer, origin=match.TIDAL))
```

New text:

```
                named.append(replace(one, ref=answer))
```

### `u79-c.C7_fixed_name`

The found list takes one fixed name, so the run after an answer is refused

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C7_fixed_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_one_exact_candidate_is_listed_without_review`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[.txt-txt-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[\xa7\xa7\xa7.txt-tracklist-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[friday set (2026).txt-friday-set-2026-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[intake-j1.unlisted.json-intake-j1-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[notes-notes-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[warmup.list.json-warmup-found]`
  - `tests/test_intake_missing_search.py::test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused`
  - `tests/test_intake_missing_search.py::test_the_unlisted_list_is_read_and_its_found_list_sits_beside_the_jobs`
  - `tests/test_intake_missing_search.py::test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide`

Old text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"
```

New text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}"
```

### `u79-c.C8_asked_is_a_no_op`

A run that only put a question to a person ends as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C8_asked_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
        outcome=Outcome.OK if listed or asked else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if listed else Outcome.NO_OP,
```

### `r1037.N1_landed_not_recorded`

_record_landing_commit: never write collection_landed, so no landed row is ever offered

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N1_landed_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`
- Collected: 86 against a baseline of 86
- Kills: 33 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_record_with_no_update_count_offers_nothing[12]`
  - `tests/test_delete_landed_removed.py::test_a_landing_record_with_no_update_count_offers_nothing[None]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    if landed is not None:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
```

New text:

```
    if False:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
```

### `r1037.N2_joined_not_made`

_landed_rows: record every playlist the rows joined, made or already there

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N2_joined_not_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`

Old text:

```
    playlists = sorted({str(one) for one in joined if one and str(one) not in before})
```

New text:

```
    playlists = sorted({str(one) for one in joined if one})
```

### `r1037.N3_identity_wrong`

_landed_rows: record no database identity

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N3_identity_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 21 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        "database_identity": plan.master_db_id,
```

New text:

```
        "database_identity": "",
```

### `r1037.N4_size_not_read`

_landed_rows: record no file size, so no landed file can be proved by its size

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N4_size_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 12 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_every_row_it_made_as_the_database_holds_it`

Old text:

```
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS},
```

New text:

```
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS if name != "FileSize"},
```

### `r1037.N5_count_before_commit`

_landed_rows: record a count short of the one the commit left

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N5_count_before_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_every_row_it_made_as_the_database_holds_it`

Old text:

```
        sequence = int(db.get_local_usn())
```

New text:

```
        sequence = int(db.get_local_usn()) - 1
```

### `r1037.N6_before_empty`

apply_rows: read no playlist before the landing, so a playlist already there is recorded as made

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N6_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`

Old text:

```
        playlists_before = frozenset(str(row.ID) for row in db.get_playlist())
```

New text:

```
        playlists_before = frozenset()
```

### `r1844.N13_landing_writes_no_uuid`

native landing: the record names each row with an empty UUID

- File: `src/cratekit/intake/native.py`
- Source: `r1844.json`, row `N13_landing_writes_no_uuid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`
- Collected: 42 against a baseline of 42
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_each_row_by_the_uuid_the_database_holds`

Old text:

```
                    LANDED_UUID_KEY: str(getattr(content, "UUID", None) or ""),
```

New text:

```
                    LANDED_UUID_KEY: "",
```

### `r746-b.N3_folder_path_not_restamped`

_restamp: the row keeps the path the binding stored, the planned path is never put on it

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N3_folder_path_not_restamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`

Old text:

```
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
```

New text:

```
    if False:
        content.FolderPath = row.folder_path
```

### `r746-b.N4_device_not_restamped`

_restamp: the row keeps the device the binding chose

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N4_device_not_restamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`

Old text:

```
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
```

New text:

```
    if False:
        content.DeviceID = plan.device_id
```

### `r777.N16_pass_not_recorded`

The native landing's commit no longer records the pass

- File: `src/cratekit/intake/native.py`
- Source: `r777.json`, row `N16_pass_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`

Old text:

```
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
```

New text:

```
    if False:
        record.detail[PASS_KEY] = plan.pass_name
```

### `r923.N1_landing_sets_nothing`

The native landing no longer sets rekordbox's defaults on a row it creates

- File: `src/cratekit/intake/native.py`
- Source: `r923.json`, row `N1_landing_sets_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`

Old text:

```
        if getattr(content, column, None) is None:
```

New text:

```
        if False:
```

### `u113-c.C1_native_batch_always`

The native write always makes the batch playlist, empty when every row was claimed

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C1_native_batch_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
            if ordered or not accounts:
```

New text:

```
            if True:
```

### `u113-c.C2_native_batch_keeps_claimed`

The native batch playlist holds the claimed rows too

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C2_native_batch_keeps_claimed`
- Moved: the same guard, the claimed test of the batch walk, now one comprehension in native.py's _batch_order (U307 folded the loop)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
        dict.fromkeys(by_target[one] for one in targets if one in by_target and one not in claimed)
```

New text:

```
        dict.fromkeys(by_target[one] for one in targets if one in by_target)
```

### `u113-c.C3_native_found_by_name`

An account playlist is found by its name under INBOX and added to, rather than created

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C3_native_found_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
                created = db.create_playlist(one.name, parent=anchor)
```

New text:

```
                created = rb_writer.ensure_playlist(db, one.name, anchor)
```

### `u113-c.C4_native_record_unnamed`

The native landing record does not list the account playlists by identifier

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C4_native_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
        record.detail[INBOX_PLAYLISTS_KEY] = [
```

New text:

```
        record.detail["inbox_playlists_unread"] = [
```

### `u115.F1_landing_keeps_random_id`

The native landing keeps the random rb_file_id the binding minted instead of the landed file's inode

- File: `src/cratekit/intake/native.py`
- Source: `u115.json`, row `F1_landing_keeps_random_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 93 against a baseline of 93
- Kills: 27 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))

```

New text:

```
(empty)
```

### `u120.N3_identity_without_hearts`

identity: the digest leaves the hearts out

- File: `src/cratekit/intake/native.py`
- Source: `u120.json`, row `N3_identity_without_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`

Old text:

```
    favorites = {"favorites": plan.favorites.identity()} if plan.favorites is not None else {}
```

New text:

```
    favorites = {}
```

### `u126.F3_counts_undigested`

Digest the value alone, so the counts the screen shows can change under an approval

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `F3_counts_undigested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`

Old text:

```
            {"value": plan.link.value, "carriers": plan.link.carriers, "rows": plan.link.rows}
```

New text:

```
            {"value": plan.link.value}
```

### `u126.P2_not_shown`

Drop ContentLink from a row's columns, so the screen and the row's part of the digest omit it

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `P2_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 77 against a baseline of 77
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_link_its_count_the_playlist_and_each_file_move_the_digest`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
            **(
                {rb_writer.CONTENT_LINK_COLUMN: self.content_link}
                if self.content_link is not None
                else {}
            ),
```

New text:

```
(empty)
```

### `u126.R1_binding_value_kept`

Drop the restamp of ContentLink, so the row keeps the binding's value

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R1_binding_value_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 106 against a baseline of 106
- Kills: 37 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 22 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    pass
```

### `u126.R2_fill_if_null`

Set ContentLink only when the binding left it NULL, which it never does

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R2_fill_if_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 106 against a baseline of 106
- Kills: 37 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 22 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    if getattr(content, rb_writer.CONTENT_LINK_COLUMN, None) is None:
        setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

### `u126.R3_check_skipped`

Skip the read back's ContentLink check

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R3_check_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_assert_rows_identified_holds_the_file_id_and_the_link_to_the_ones_planned`

Old text:

```
        if landed.content_link is None or row.content_link != landed.content_link
```

New text:

```
        if False
```

### `u126.R5_read_back_file_id`

Read back the file id column where the link should be

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R5_read_back_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 106 against a baseline of 106
- Kills: 37 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 22 more, see the JSON sidecar

Old text:

```
        None if row[3] is None else int(row[3]),
```

New text:

```
        None if row[2] is None else int(row[2]),
```

### `u126.S1_file_id_kept`

Sample, U115: drop the file id restamp, so the row keeps the binding's random id

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S1_file_id_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 106 against a baseline of 106
- Kills: 38 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))
```

New text:

```
    pass
```

### `u126.S2_defaults_left_null`

Sample, R-923: drop the defaults fill, so the binding's NULLs stay

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S2_defaults_left_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`

Old text:

```
        if getattr(content, column, None) is None:
            setattr(content, column, value)
```

New text:

```
        pass
```

### `u127-b.N6b_digest_blind_to_vox`

Drop each added row's score and answer from the digest, after the engine test

- File: `src/cratekit/intake/native.py`
- Source: `u127-b.json`, row `N6b_digest_blind_to_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_engine_digest_covers_each_rows_score_and_answer`

Old text:

```
                "rows": [[str(row.target), row.voxlevel, row.vox] for row in plan.to_add()],
```

New text:

```
                "rows": [[str(row.target)] for row in plan.to_add()],
```

### `u127.N10_record_silent`

Record no commit under the vocals key, so a restore cannot count the tags

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N10_record_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    if vox_written > 0:
```

New text:

```
    if vox_written > 10**6:
```

### `u127.N11_missing_unreported`

Never report a planned tag that adoption does not read back

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N11_missing_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
```

New text:

```
            row.target for row, content_id in added_ids if False
```

### `u127.N12_unscored_dropped`

Name no unscored file on the landed record

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N12_unscored_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`

Old text:

```
    unscored = {row.target for row in plan.vox_unscored()}
```

New text:

```
    unscored = set()
```

### `u127.N14_read_back_skipped`

Never read the tag back, so every landed row reports untagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N14_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`
- Collected: 49 against a baseline of 49
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

New text:

```
            (frozenset(), "") if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

### `u127.N7_digest_blind_to_cut`

Drop the cut from the digest

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N7_digest_blind_to_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_and_the_digest_moves_with_a_tag_and_the_cut`

Old text:

```
                "cut": plan.vox_cut,
```

New text:

```
                "cut": None,
```

### `u127.N8_tag_never_written`

Write no tag at the apply, the defect R-841 measured

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N8_tag_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`
- Collected: 49 against a baseline of 49
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_library_with_another_category_only_gains_the_vocals_category`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            vox_written = _tag_vox(db, added_ids)
```

New text:

```
            vox_written = 0
```

### `u127.N9_tag_every_added`

Write the tag on every added row, not only those the plan tagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N9_tag_every_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`
- Collected: 122 against a baseline of 122
- Kills: 50 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_of_the_twentieth_of_october_joins_its_month_and_an_undated_one_undated`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - ... and 35 more, see the JSON sidecar

Old text:

```
    content_ids = [content_id for row, content_id in added if row.vox]
```

New text:

```
    content_ids = [content_id for row, content_id in added]
```

### `u128-b.N1_native_owned_unwritten`

The native commit joins no owned row to its playlist, the new rows alone

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N1_native_owned_unwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
                        member.content_id
                        if member.target is None
```

New text:

```
                        ""
                        if member.target is None
```

### `u128-b.N2_native_record_no_pass`

The native landing's record names no pass, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N2_native_record_no_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
```

New text:

```
                ingest.INBOX_PASS_KEY: "",
```

### `u146-c.N2_owned_not_written`

apply_rows: the owned hearts are planned and shown and never written

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N2_owned_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
```

New text:

```
(empty)
```

### `u146-e.N3_owned_out_of_digest`

FavoritesPlan.identity: the owned hearts are not digested, so an answer given for one set of them stands for another

- File: `src/cratekit/intake/native.py`
- Source: `u146-e.json`, row `N3_owned_out_of_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.owned:
            identity["owned"] = [
```

New text:

```
        if self.owned and False:
            identity["owned"] = [
```

### `u150.F2_record_provider`

native._record_commit: write no provider tracks on the landing's record

- File: `src/cratekit/intake/native.py`
- Source: `u150.json`, row `F2_record_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror`

Old text:

```
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
```

New text:

```
        pass
```

### `u153.N1_restamp_id_text`

native _restamp: do not coerce the minted ID to text, so a colour on an existing row cannot flush beside a new one

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N1_restamp_id_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_owned_hearts_native.py`
- Collected: 25 against a baseline of 25
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
    content.ID = str(content.ID)
```

New text:

```
    content.ID = content.ID
```

### `u153.N3_landing_colour_owned`

native apply: drop the owned hearts from the colour set, so an owned heart is placed but not coloured

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N3_landing_colour_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                to_colour.extend(plan.favorites.colour)
```

New text:

```
                to_colour.extend([])
```

### `u156.L18_digest_native`

native.identity: leave the label plan out of the landing's digest

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L18_digest_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_manifests_bytes`
  - `tests/test_intake_land_labels_native.py::test_the_label_source_moves_the_digest_and_an_answer_for_one_is_stale_for_another`

Old text:

```
    filed = {"labels": label_filing.identity(plan.labels)} if plan.labels is not None else {}
```

New text:

```
    filed = {}
```

### `u156.L19_write_called`

apply_rows: plan the labels and never write them

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L19_write_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 17 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist[2021]`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere_and_not_said_to_be_in_the_intake_playlist[None]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2020]`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest[2021]`
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_and_a_decomposed_label_is_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_the_move_refused_is_said_not_to_have_landed`
  - `tests/test_intake_land_labels_native.py::test_label_files_each_file_once_under_the_year_its_date_tag_names`
  - `tests/test_intake_land_labels_native.py::test_one_label_spelled_two_ways_is_one_folder_and_a_file_two_rows_file_names_both_years`
  - ... and 2 more, see the JSON sidecar

Old text:

```
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
```

New text:

```
                labels_written = None
```

### `u156.L20_recorded`

_record_landing_commit: write the labels and record nothing of them on the session

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L20_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`

Old text:

```
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
```

New text:

```
    if False:
        label_filing.record_commit(record, labels_written, cfg)
```

### `u157.N2_digest_rows`

identity: the dyn block names each row's answer only, not its drift or verdict

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N2_digest_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_engine_digest_covers_each_rows_drift_verdict_and_answer`

Old text:

```
[str(row.target), row.drift, row.drift_verdict, row.dyn]
```

New text:

```
[str(row.target), row.dyn]
```

### `u157.N3_no_write`

apply: the dyn tag is never written

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N3_no_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[exactly-at-the-cut]`
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[moving]`
  - `tests/test_intake_land_dyn_native.py::test_a_landing_whose_every_row_is_dyn_says_the_visit_ends_on_dynamic`
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
            dyn_written = _tag_dyn(db, added_ids)
```

New text:

```
            dyn_written = 0
```

### `u157.N4_trust_the_writer`

apply: report each row's dyn from the plan, not the read back

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N4_trust_the_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_tag_written_under_a_removed_value_is_said_and_never_counted`

Old text:

```
                    dyn=content_id in dyned,
```

New text:

```
                    dyn=row.dyn,
```

### `u157.N5_no_record`

_record_landing_commit: record no dyn tags on the session

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N5_no_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
    if dyn_written > 0:
        session.record_commit(
```

New text:

```
    if False:
        session.record_commit(
```

### `u161.P1_path_back_in_digest`

native.identity: digest str(plan.database) again, the line U161 removed, so a copy rehearsal can never match

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P1_path_back_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "database": str(plan.database),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P2_parent_in_digest`

native.identity: digest the database's folder under another key, a path the old key's name check would not see

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P2_parent_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "where": str(plan.database.parent),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P3_file_name_in_digest`

native.identity: digest the database's file name alone, which a copy named differently from master.db would not share

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P3_file_name_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "file": plan.database.name,
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P4_device_out`

native.identity: drop the device, so an answer for one library is not stale for another with the same master id

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P4_device_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "master_db_id": plan.master_db_id,
```

### `u161.P5_master_out`

native.identity: drop the master id, the other half of the library identity that replaced the path

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P5_master_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "device": plan.device_id,
```

### `u161.S1_playlist_out`

native.identity: drop the batch playlist's name from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S1_playlist_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "playlist": plan.playlist,
        "batch_playlist": plan.batch_playlist_id,
```

New text:

```
        "batch_playlist": plan.batch_playlist_id,
```

### `u161.S2_columns_out`

native.identity: drop each row's columns from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S2_columns_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
                "content_id": row.content_id,
                "columns": row.columns(),
```

New text:

```
                "content_id": row.content_id,
```

### `u163.W12_readback_active`

_words_back: read the artist through any row, tombstones included

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W12_readback_active`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`

Old text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} AND a.{active} "
```

New text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} "
```

### `u163.W13_identified_words`

assert_rows_identified: never compare the words read back

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W13_identified_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_landed_row_whose_word_reads_back_wrong_is_refused`

Old text:

```
        if row.words.get(column) != want
```

New text:

```
        if False
```

### `u163.W14_album_artist_link`

_Mints._mint: mint an album with no album artist

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W14_album_artist_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`

Old text:

```
        if word.table == rb_writer.ALBUM_TABLE:
            columns[ALBUM_ARTIST]
```

New text:

```
        if False:
            columns[ALBUM_ARTIST]
```

### `u163.W4_year_written`

_Mints.link: drop the ReleaseYear write

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W4_year_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`

Old text:

```
        if row.year is not None:
            setattr(content, YEAR_COLUMN, row.year)
```

New text:

```
        if False:
            setattr(content, YEAR_COLUMN, row.year)
```

### `u163.W7_unmoved`

_assert_words_unmoved: never refuse a word that moved since the plan

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W7_unmoved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`

Old text:

```
            if _rows_of(now) != _rows_of(word):
```

New text:

```
            if False:
```

### `u163.W8_mint_once`

_Mints.id_of: mint a new word again for every row

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W8_mint_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`

Old text:

```
        if key not in self._made:
            self._made[key] = self._mint(word)
```

New text:

```
        if True:
            self._made[key] = self._mint(word)
```

### `u163.W9_creations_named`

apply_rows: name only the content table in creations, so a mint is refused

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W9_creations_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_words.py`
- Collected: 62 against a baseline of 62
- Kills: 23 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[None]`
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_file_id_lies_once]`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_or_link_did_not_take_is_refused_after_the_commit[_link_keeps_the_bindings]`
  - `tests/test_intake_land_native.py::test_a_second_approved_run_over_the_landed_files_adds_nothing`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - ... and 8 more, see the JSON sidecar

Old text:

```
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
```

New text:

```
                db, creations=(rb_writer.CONTENT_TABLE,)
```

### `u164.R1_record_filed`

_record_landing_commit: never record the filed batch and its folder

- File: `src/cratekit/intake/native.py`
- Source: `u164.json`, row `R1_record_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 75 against a baseline of 75
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_landing_on_the_27th_lands_in_its_year_folder_under_its_subject`
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`

Old text:

```
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY]
```

New text:

```
    if False:
        record.detail[FILED_BATCH_KEY]
```

### `u165.N1_digest`

identity: leave the predictions out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u165.json`, row `N1_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`
- Collected: 10 against a baseline of 10
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_rehearsal_digests_as_the_live_landing_that_files_and_land_only_apart`

Old text:

```
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
```

New text:

```
        {}
```

### `u166.A4_no_add`

apply_rows: add nothing to Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A4_no_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 120 against a baseline of 120
- Kills: 13 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
```

New text:

```
            if False:
                analyze = _analyze_row(db, plan, anchor)
```

### `u166.A5_present_rows_too`

apply_rows: add every row the plan names, present ones too

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A5_present_rows_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`

Old text:

```
                        db, analyze, [content_id for _row, content_id in added_ids]
```

New text:

```
                        db, analyze, list(by_target.values())
```

### `u166.A6_always_create`

_analyze_row: make a new Analyze every landing

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A6_always_create`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`

Old text:

```
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)
```

New text:

```
    return db.create_playlist(ANALYZE, parent=anchor)
```

### `u166.A7_record_count`

apply_rows: record the batch's memberships only on success

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A7_record_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 104 against a baseline of 104
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
```

New text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships,
```

### `u166.A8_digest_key`

identity: leave the found Analyze out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A8_digest_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`

Old text:

```
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
```

New text:

```
    analyze = {}
```

### `u307.R23_batch_order_keeps_claimed`

native._batch_order: rows an account playlist claimed join the batch playlist as well

- File: `src/cratekit/intake/native.py`
- Source: `u307.json`, row `R23_batch_order_keeps_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
by_target[one] for one in targets if one in by_target and one not in claimed)
```

New text:

```
by_target[one] for one in targets if one in by_target)
```

### `u954.M8_no_category_order`

DYN_NO_CATEGORY: the refusal's by hand Dynamic run placed after the Normal run

- File: `src/cratekit/intake/native.py`
- Source: `u954.json`, row `M8_no_category_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    "rows this landing names with Analysis Mode Dynamic by hand, before any Normal "
```

New text:

```
    "rows this landing names with Analysis Mode Dynamic by hand, after any Normal "
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
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
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
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`

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
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
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
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 77 against a baseline of 77
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
- Ran: `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`
- Collected: 49 against a baseline of 49
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
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
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
- Ran: `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`
- Collected: 49 against a baseline of 49
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
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
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
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
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
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
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
- Ran: `tests/test_intake_land_dyn_native.py`
- Collected: 17 against a baseline of 17
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
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
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
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
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
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land_words.py`
- Collected: 62 against a baseline of 62
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
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
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
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
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
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
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
- Ran: `tests/test_intake_land_words.py`
- Collected: 18 against a baseline of 18
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
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

### `r1255.F1_refill_plan_unlisted`

plan_refill: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/refill.py`
- Source: `r1255.json`, row `F1_refill_plan_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`

Old text:

```
        log_unlisted=session.log_unlisted(unreadable, cfg),
```

New text:

```
        log_unlisted=False,
```

### `u134-a.A10_shared_playlist`

Let two jobs share one playlist unless three do

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A10_shared_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_asked_only_of_a_playlist_no_record_gives_another_pass_and_only_if_read`

Old text:

```
counts[one.playlist_id] > 1
```

New text:

```
counts[one.playlist_id] > 2
```

### `u134-a.A11_pass_unknown`

Drop the refusal of a pass with no account playlist job

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A11_pass_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`

Old text:

```
    if not named:
        raise _pass_unknown(cfg, pass_name)

```

New text:

```
(empty)
```

### `u134-a.A1_outside_inbox`

Drop the refusal of a recorded mirror that is live outside INBOX

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A1_outside_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`

Old text:

```
        if str(mirror.ID) not in under:
```

New text:

```
        if False:
```

### `u134-a.A2_mirror_is_first`

Take the newest recorded entry of the pass as the mirror instead of the oldest

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A2_mirror_is_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`

Old text:

```
        mirror = _live_playlist(db, recorded[0])
```

New text:

```
        mirror = _live_playlist(db, recorded[-1])
```

### `u134-a.A3_gone_listed`

Fall through to the name match when the recorded mirror is gone

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A3_gone_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`

Old text:

```
    if recorded:
        mirror = _live_playlist(db, recorded[0])
```

New text:

```
    if recorded and _live_playlist(db, recorded[0]) is not None:
        mirror = _live_playlist(db, recorded[0])
```

### `u134-a.A4_others_excluded`

Let the name match take a playlist a record gives another pass

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A4_others_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_asked_only_of_a_playlist_no_record_gives_another_pass_and_only_if_read`

Old text:

```
            if key not in others
```

New text:

```
            if True
```

### `u134-a.A5_unreadable`

Trust a name match while a session record could not be read

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A5_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_asked_only_of_a_playlist_no_record_gives_another_pass_and_only_if_read`

Old text:

```
        if unreadable:
```

New text:

```
        if False:
```

### `u134-a.A6_pre_u128_exact_name`

Match a pre U128 entry by pass alone, so the Name 2 twin counts

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A6_pre_u128_exact_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`

Old text:

```
    return entry.account == account if entry.account else entry.name == name
```

New text:

```
    return entry.account == account if entry.account else True
```

### `u134-a.A7_pass_matched`

Drop the pass comparison, so another pass's record names the mirror

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A7_pass_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`

Old text:

```
    if entry.pass_name != pass_name:
        return False

```

New text:

```
(empty)
```

### `u134-a.A8_only_what_it_lacks`

Plan every distinct member as an add whatever the playlist holds

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A8_only_what_it_lacks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`

Old text:

```
if one not in present)
```

New text:

```
if True)
```

### `u134-b.B1c_composite_short_write`

What B1 holds: the write adds all but the first planned membership

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B1c_composite_short_write`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 7 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`

Old text:

```
                    rb_writer.add_memberships(db, playlist, target.adds)
```

New text:

```
                    rb_writer.add_memberships(db, playlist, target.adds[1:])
```

### `u134-b.B2c_composite_reversed_write`

What B2 holds: the write adds the planned memberships in reverse

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B2c_composite_reversed_write`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 7 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`

Old text:

```
                    rb_writer.add_memberships(db, playlist, target.adds)
```

New text:

```
                    rb_writer.add_memberships(db, playlist, target.adds[::-1])
```

### `u134-b.B4_record_on_success`

Drop the success path's record of the commit

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B4_record_on_success`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`

Old text:

```
        _record_refill_commit(record, plan, added, cfg)
        convergence.record_fingerprint(cfg, db)
```

New text:

```
        convergence.record_fingerprint(cfg, db)
```

### `u134-b.B7_again_action`

Show a repeated track's second row as held, not again

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B7_again_action`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`

Old text:

```
            if one.content_id in seen:
```

New text:

```
            if False:
```

### `u175.F1_bridge_name_unasked`

refill.locate: ask only the account's bare name again, so a dated playlist an intake file recorded by name alone is called unfound

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F1_bridge_name_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`

Old text:

```
        asked = {name, recorded_name} - {"", native.ANALYZE}
```

New text:

```
        asked = {name} - {"", native.ANALYZE}
```

### `u175.F2_bridge_names_any_account`

refill.bridge_names: take an intake file's entry of any account, so another account playlist's dated name is asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F2_bridge_names_any_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
                and str(entry.get(ingest.INBOX_ACCOUNT_KEY) or "") == account
```

New text:

```
                and True
```

### `u175.F3_analyze_asked`

refill.locate: stop excluding the reserved Analyze from the names asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F3_analyze_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`

Old text:

```
        asked = {name, recorded_name} - {"", native.ANALYZE}
```

New text:

```
        asked = {name, recorded_name} - {""}
```

### `u175.F4_bridge_names_any_state`

refill.bridge_names: read an intake record that no longer stands, so an abandoned landing's name is asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F4_bridge_names_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW or record.state not in _STANDING:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if (
```

New text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if (
```

### `u175.F5_bridge_names_by_id_order`

refill.bridge_names: order the records by identifier alone, so a later landing whose identifier sorts first is asked as the first

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F5_bridge_names_by_id_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
    names: list[str] = []
    for record in sorted(records, key=lambda one: (one.started, one.session_id)):
```

New text:

```
    names: list[str] = []
    for record in sorted(records, key=lambda one: one.session_id):
```

### `r1255.F2_refill_warning_wording`

warnings_of: word an unlisted log as a count of records

- File: `src/cratekit/intake/refill_cli.py`
- Source: `r1255.json`, row `F2_refill_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_matches_by_name_and_an_unlisted_log_is_named_as_one`

Old text:

```
                        if plan.log_unlisted
```

New text:

```
                        if False
```

### `u134-b.B5_no_writes_no_op`

Apply a plan that adds nothing instead of ending no_op

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B5_no_writes_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u134-b.B6_ack_before_gate`

Drop the backup acknowledgment read before the plan and the gate

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B6_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `u307.R10_refill_writing_watches_nothing`

refill_cli.writing: hand the write no analysis roots, so refill and analyzed apply with an empty analysis watch

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u307.json`, row `R10_refill_writing_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 27 against a baseline of 27
- Kills: 13 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_then_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_then_a_lost_track_is_left`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_in_account_order_and_once`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_are_neither_filled_and_one_is_found_by_it`

Old text:

```
        return apply(db, analysis_store.watch_roots(cfg))
```

New text:

```
        return apply(db, ())
```

### `u331.S09_rehearsal_origin_renamed`

intake/rehearsal: print the package it moved to as the rehearsal's refusal origin

- File: `src/cratekit/intake/rehearsal.py`
- Source: `u331.json`, row `S09_rehearsal_origin_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
_ORIGIN = ("core", "rehearsal")
```

New text:

```
_ORIGIN = ("intake", "rehearsal")
```

### `u331.S10_check_engine_imports_analysis_at_top`

intake/rekordbox_check: import the analysis package at the top again, so analyze check cannot build with the analysis toggle off

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u331.json`, row `S10_check_engine_imports_analysis_at_top`
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
from typing import Any, Iterable, Mapping, Sequence

from cratekit.core import analysis_store,
```

New text:

```
from typing import Any, Iterable, Mapping, Sequence

from cratekit.analysis import agreement  # noqa: F401
from cratekit.core import analysis_store,
```

### `r1255.R1_rotation_unlisted_from_scan`

landings: never read the listing off the scan, so the classifier's reason counts one record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R1_rotation_unlisted_from_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
    unlisted = session.log_unlisted(unreadable, cfg)
```

New text:

```
    unlisted = False
```

### `r1255.R2_plan_carries_unlisted`

plan_rotation: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R2_plan_carries_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        log_unlisted=found.unlisted,
```

New text:

```
        log_unlisted=False,
```

### `u111-c.C3_inboxed_suffix`

A name ending _inboxed is no longer recognised as a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C3_inboxed_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    if name.endswith(INBOXED_SUFFIX):
```

New text:

```
    if False:
```

### `u111-c.C4_removal_threshold`

A batch in Old is removed after the stale threshold instead of the expired one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C4_removal_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
        action = REMOVE if age > expired_days else KEEP
```

New text:

```
        action = REMOVE if age > stale_days else KEEP
```

### `u111-c.C5_move_threshold`

A batch in INBOX moves only after the expired threshold instead of the stale one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C5_move_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
        action = MOVE if age > stale_days else KEEP
```

New text:

```
        action = MOVE if age > expired_days else KEEP
```

### `u111-c.C6_plan_taken_again`

The write no longer takes the plan again on its own handle and compares digests

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C6_plan_taken_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_inbox_changed_after_the_approval_is_refused_and_nothing_is_written`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u111-c.C7_old_creation_planned`

The folder the write creates for Old is not named to the confinement judge

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C7_old_creation_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`

Old text:

```
                created.append(str(old.ID))
```

New text:

```
                pass
```

### `u111-d.C10_two_olds_refused`

Two live Old folders under INBOX are no longer refused, the first is used

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C10_two_olds_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_empty_inbox_still_asks_then_no_old_declared_or_two_olds_are_refused_by_name`

Old text:

```
    if len(olds) > 1:
```

New text:

```
    if len(olds) > 99:
```

### `u111-d.C9_committed_records_only`

A landing record dates its batch whether or not its commit landed

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C9_committed_records_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_landing_record_that_committed_nothing_dates_nothing`

Old text:

```
        if str(session.SourceState.COMMITTED) not in {str(v) for v in record.sources.values()}:
```

New text:

```
        if False:
```

### `u113-c.C7_unproven_import_names`

The rotation reads an intake file's recorded names whether or not its import was proven

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C7_unproven_import_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_a_recorded_name_whose_batch_folder_is_gone_is_left_alone[never-imported]`

Old text:

```
        if session.IMPORT_VERIFIED_KEY in record.detail:
```

New text:

```
        if True:
```

### `u113-c.C9_earliest_name_wins`

The earliest landing of a recorded name ages it, not the latest

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C9_earliest_name_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_the_latest_landing_of_a_name_is_the_one_it_is_aged_by`

Old text:

```
                if name not in by_name or landed >= by_name[name][0]:
```

New text:

```
                if name not in by_name or landed <= by_name[name][0]:
```

### `u166.R2_rotate_reserved`

_classify: let the rotation take Analyze for a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u166.json`, row `R2_rotate_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_rotation_never_takes_analyze_for_a_batch_whatever_a_record_says`

Old text:

```
    if not in_old and name == native.ANALYZE:
```

New text:

```
    if False:
```

### `u175.R1_account_ids_unrecorded`

rotate._named_ids: read no account playlist off a native landing record, so a dated playlist is no batch and is neither rotated nor mirrored

- File: `src/cratekit/intake/rotate.py`
- Source: `u175.json`, row `R1_account_ids_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 16 against a baseline of 16
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
```

New text:

```
    accounts = None
    if isinstance(accounts, list):
```

### `u214.M15_unread_is_not_none`

_classify: say no landing record names an unrecognised playlist even while a session record could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M15_unread_is_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
            if unread
            else
```

New text:

```
            if False
            else
```

### `u214.M16_old_only_under_inbox`

_classify: read a folder named Old inside Old as the Old folder too

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M16_old_only_under_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if old_display is not None and name == old_display:
```

### `u214.M18_folder_unknown`

_batch_folder: read a refused batch folder as absent, so a batch is said to have none

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M18_folder_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
    except OSError:
        return None
```

New text:

```
    except OSError:
        return False
```

### `u214.M19_folder_unread_reason`

_classify: say no batch folder carries the name even while the music folder could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M19_folder_unread_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
            if folder_unread

```

New text:

```
            if False

```

### `u214.M1_old_named_as_old`

_classify: never name the declared Old as Old, so it reads as any folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M1_old_named_as_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if False:
```

### `u214.M20_unread_unlisted`

Landings.unread: say nothing of a log that could not be listed

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M20_unread_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        if self.unlisted:
```

New text:

```
        if False:
```

### `u214.M2_left_row_count`

_classify: count no rows for a left playlist, so the unrecognised label playlist is named without its 36 rows

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M2_left_row_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_payload_shows_each_left_node_with_its_row_count`

Old text:

```
        tracks = _track_count(db, row) if counted else None
```

New text:

```
        tracks = None
```

### `u214.M3_live_left_collected`

live_batches: collect no left node, so the mirror drops them unsaid again

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M3_live_left_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_inbox_unmirrored.py::test_an_undeclared_old_is_named_as_a_folder`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        else:
            left.append(classified)
    return Live(
```

New text:

```
        else:
            pass
    return Live(
```

### `u214.M4_digest_without_count`

identity: digest each left node with its row count, so adding a track to a person's playlist stales the rotation gate

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M4_digest_without_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`

Old text:

```
        "left": [node.identity() for node in plan.left],
```

New text:

```
        "left": [node.to_json() for node in plan.left],
```

### `u214.M5_rotation_old_display`

plan_rotation: pass no Old display, so the rotation plan names Old as a folder and the mirror as Old

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M5_rotation_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
            old_display=old.display,
```

New text:

```
            old_display=None,
```

### `u214.M6_live_old_display`

live_batches: read no Old display, so the mirror names Old as a plain folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M6_live_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
    old_display = declared.intake_old.display if declared.intake_old is not None else None
```

New text:

```
    old_display = None
```

### `u214.M7_label_rows`

Left.label: leave the row count out of the line a person reads

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M7_label_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`

Old text:

```
        rows = f" ({self.tracks} row(s))" if self.tracks is not None else ""
```

New text:

```
        rows = ""
```

### `u307.R8_anchored_root_drops_cutover_step`

rotate.anchored_root: the bridge refusal shared by every INBOX writer no longer names crate tree cutover as its step

- File: `src/cratekit/intake/rotate.py`
- Source: `u307.json`, row `R8_anchored_root_drops_cutover_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`
  - `tests/test_inbox_rotate.py::test_an_intake_tree_on_the_bridge_is_refused_naming_the_cutover`

Old text:

```
                f"run crate tree cutover {tree_id} --export with a Fresh Export to "
                f"move the intake tree to the database",
```

New text:

```
                "move the intake tree to the database",
```

### `u329.W3_rotate_holds_a_permissive_copy`

intake.rotate binds a watched_roots of its own that accepts an empty list, the copy the one home replaced

- File: `src/cratekit/intake/rotate.py`
- Source: `u329.json`, row `W3_rotate_holds_a_permissive_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_empty_analysis_watch_is_refused_for_every_write_that_shares_it`

Old text:

```
from cratekit.write.row_defaults import watched_roots

```

New text:

```
def watched_roots(roots):
    return [Path(root) for root in roots]

```

### `r1255.R3_rotation_warning_gate`

records_warnings: never warn, so the rotation ages a batch from its playlist's date unsaid

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R3_rotation_warning_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
    if not plan.unreadable_records:
        return []
    unread = (
```

New text:

```
    if True:
        return []
    unread = (
```

### `r1255.R4_rotation_warning_wording`

records_warnings: word an unlisted log as a count of records

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R4_rotation_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        if plan.log_unlisted
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

New text:

```
        if False
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

### `u111-d.D1_empty_plan_asks`

A plan that moves and removes nothing returns without asking the gate

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u111-d.json`, row `D1_empty_plan_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1050 against a baseline of 1050
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[inbox.rotate]`
  - `tests/test_inbox_rotate.py::test_an_empty_inbox_still_asks_then_no_old_declared_or_two_olds_are_refused_by_name`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "approve":
```

New text:

```
    if plan.writes and ctx.gate.require(spec, plan=data, context=_facts(plan)) != "approve":
```

### `u111-d.D2_ack_before_gate`

The backup acknowledgment is no longer read before the plan and the gate

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u111-d.json`, row `D2_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    pass
```

### `r1017.M3_landing_open_read`

Landing records: read a record that never closed as a landing

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M3_landing_open_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[open]`

Old text:

```
        if record.state is session.SessionState.CLOSED
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        if record.state is not None
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

### `r1017.M4_landing_uncommitted_read`

Landing records: read a record whose source never committed as a landing

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M4_landing_uncommitted_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[uncommitted]`

Old text:

```
        and str(session.SourceState.COMMITTED) in record.sources.values()
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        and record.sources
        and isinstance(record.detail.get(RECORD_KEY), Mapping)
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

### `r1017.M5_landing_any_job`

Landing records: read another job's landing as this job's

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M5_landing_any_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_with_no_landing_record_and_no_matching_name_still_refuses[another job]`
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        and record.detail[RECORD_KEY].get("job") == job_id
    ]
    return tuple(
```

New text:

```
        and record.detail[RECORD_KEY].get("job") is not None
    ]
    return tuple(
```

### `r1017.M6_oldest_first`

Landing records: read them oldest first, which recorded_playlist also depends on

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M6_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=True)
```

New text:

```
        for record in sorted(found, key=lambda one: one.session_id, reverse=False)
```

### `r1017.M7_names_not_deduplicated`

recorded_names: return a name twice when two landings recorded it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `r1017.json`, row `M7_names_not_deduplicated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_recorded_names_reads_every_landing_of_the_job_the_newest_first`

Old text:

```
        dict.fromkeys(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

New text:

```
        list(name for kept in _landed(cfg, job_id) if (name := str(kept.get("name") or "")))
```

### `u154.G10_read_back_path_unchecked`

a row committed with a path other than the planned one is reported as shelved

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G10_read_back_path_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            if str(stored or "") != row.folder_path:

```

New text:

```
            if False:

```

### `u154.G11_kept_columns_unchecked`

a column the shelve does not own may change without the read back saying so

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G11_kept_columns_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`

Old text:

```
            if before.get(row.content_id) != after.get(row.content_id):

```

New text:

```
            if False:

```

### `u154.G14_reserved_folders_are_candidates`

the processed tree and the sets folder are planned as batches under --all

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G14_reserved_folders_are_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
        if entry.name.startswith(".") or entry.name in reserved:

```

New text:

```
        if entry.name.startswith("."):

```

### `u154.G15_stored_target_under_mounted_path`

the confinement check reads under the mounted target and not the stored one

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G15_stored_target_under_mounted_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`

Old text:

```
            {"prefix": _like_prefix(one.stored_target)},

```

New text:

```
            {"prefix": _like_prefix(str(one.target))},

```

### `u154.G17_refusal_before_rename_rewrapped`

a stale plan refusal before any rename is rewrapped as a write failure

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G17_refusal_before_rename_rewrapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
            if not moved and isinstance(exc, CratekitError):

```

New text:

```
            if False:

```

### `u154.G1_policy_not_registered`

the path column is written with no field policy registered for the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G1_policy_not_registered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_keeps_the_rest_and_the_name_stays_taken`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
            if True:
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

### `u154.G2_confinement_dropped`

the SQL confinement check is skipped before the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G2_confinement_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`

Old text:

```
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
                rb_writer.commit_guarded(db)

```

### `u154.G3_rename_back_dropped`

a failure past the rename leaves the folder at its new name

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G3_rename_back_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 23 against a baseline of 23
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_refuses_the_commit_and_the_free_target_rule_passes_it_over`
  - `tests/test_intake_shelve.py::test_every_refusal_and_failure_leaves_the_batch_and_its_rows_as_they_were`

Old text:

```
            failed = _rename_back(moved)

```

New text:

```
            failed: list[str] = []

```

