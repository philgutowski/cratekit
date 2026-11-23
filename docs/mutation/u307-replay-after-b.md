# Mutation table: u307-replay-after-b

Measured by `scripts/mutate.py` on 2026-11-22 23:25 UTC, branch `HEAD` at `fcbcfa11`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22539 collected. pytest invocations for this batch: 331.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 66, each measured by this driver.

Known failures: 252 node ids whose failure is this machine's and not the tree's, read from `/tmp/known-u307.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22539 against 22539. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1467.M19_root_unreadable_refuses` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M20_retired_file_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M21_native_record_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1467.M22_proof_is_a_file` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 275 | 1 | killed |
| `r1677.L1_rehearsal_unmeasured` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `r1677.L2_rehearsal_room_silent` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `r1677.L3_rehearsal_other_failure_sound` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `r501-b.L1_unretired_name` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 130 | 3 | killed |
| `r677-b.V4_after_the_stale_test` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r677.V1_no_preflight_before_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 7 | killed |
| `r677.V2_preflight_on_a_plan_of_nothing` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r677.V3_refusal_never_replaces_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 5 | killed |
| `r677.V5_preflight_raises_directly` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 2 | killed |
| `r677.V6_manifest_rows_not_handed_over` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r770-b.B1_landing_never_takes_the_native_path` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 44 | 28 | killed |
| `r770-b.B3_an_abort_writes` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `u110-b.B1_pass_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 5 | killed |
| `u110-b.B2_name_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 18 | killed |
| `u110-b.B3_check_pass` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 5 | killed |
| `u110-b.B4_recheck_xml` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `u110-b.B5_recheck_native` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `u110-b.B6_intake_lock` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `u110-b.B7_name_overrides` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 27 | killed |
| `u110-b.B8_shown_playlist` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `u113-b.B7_digest_blind_to_split` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 53 | 2 | killed |
| `u113-b.B8_pending_names_unheld` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u120.C1_no_skip_note` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 13 | 2 | killed |
| `u120.C2_hearts_not_claimed` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 13 | 10 | killed |
| `u121-b.S20r_bridge_set` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u126.P3_gate_fact` | `src/cratekit/intake/land_native.py` | user | 10 file(s) | 438 | 4 | killed |
| `u127.L1_screen_line_blind` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L2_items_carry_no_vox` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 6 | killed |
| `u127.L3_totals_from_writer` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L4_missing_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L5_unscored_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L6_bridge_ignores_calibration` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L7_land_warnings_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 7 | killed |
| `u128-b.B3_owned_unresolved_at_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 4 | killed |
| `u128-b.N3_native_owned_not_found` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 3 | killed |
| `u128.L1_bridge_warning_unsaid` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `u128.L2_native_warning_unsaid` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 2 | killed |
| `u129-author.A19_plan_archive_always_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 3 | killed |
| `u129-author.A4_archive_raise_fails_landing` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u129-author.A5_archive_return_discarded` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 76 | 2 | killed |
| `u135.A3_found_vs_made_collapsed` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 9 | 6 | killed |
| `u146-c.L2_empty_landing_no_op` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 12 | 4 | killed |
| `u146-c.L3_gate_asked_for_nothing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 2 | killed |
| `u146-c.L4_missing_source_refuses` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u153.L1_facts_colour_count` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 25 | 1 | killed |
| `u153.L3_notes_colour_skipped` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 13 | 1 | killed |
| `u156.L23_label_beside_manifest` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 90 | 1 | killed |
| `u156.L24_label_on_the_bridge` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 117 | 2 | killed |
| `u157.L1_selection_counts` | `src/cratekit/intake/land_native.py` | user | 5 file(s) | 186 | 1 | killed |
| `u157.L2_blocked_unnamed` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 126 | 1 | killed |
| `u161.L1_landing_pins_nothing` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 44 | 1 | killed |
| `u161.P6_screen_drops_path` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 44 | 2 | killed |
| `u162.L10_interrupt_cancel` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.L12_rehearsal_equal` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.L1_bridge_refusal` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.L2_area_plan_compare` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u162.L4_occupied_hold` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.L6_gridless_read_back` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.L7_identified_read_back` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.L8_success_witness` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u162.L9_kept_area_named` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 4 | killed |
| `u164.H1_watch_recorded` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u164.H2_scratch_folder` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 18 | killed |
| `u165.L1_bridge_skip` | `src/cratekit/intake/land_native.py` | user | 4 file(s) | 135 | 2 | killed |
| `u165.L2_land_only` | `src/cratekit/intake/land_native.py` | user | 4 file(s) | 135 | 3 | killed |
| `u165.L3_filing_tail` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 135 | 3 | killed |
| `u165.L4_files_into` | `src/cratekit/intake/land_native.py` | user | 4 file(s) | 135 | 2 | killed |
| `u166.A11_warning_names_batch` | `src/cratekit/intake/land_native.py` | user | 7 file(s) | 185 | 3 | killed |
| `u177.C3_flag_beside_label` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u177.C4_flag_ignored` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 46 | 4 | killed |
| `u181.L1_half_is_a_warning` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u181.L2_coefficient` | `src/cratekit/intake/land_native.py` | user | 1 file(s) | 16 | 1 | killed |
| `u188.M10_detail_mapped_dropped` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u188.M11_fields_last_part` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M12_fields_keep_indices` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M1_stored_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M2_scratch_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M3_live_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M4_staging_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 18 | killed |
| `u188.M6_mapped_as_lines` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M7_signs_swapped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M8_fields_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M9_pairs_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u319.M9_warning_drops_the_short_path` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 74 | 1 | killed |
| `u72-b.M20_shown_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M21_empty_to_engine` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72-b.M22_listing_without_isdir` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M10_default_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 19 | killed |
| `u72.M1_abort_applies` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M2_empty_plan_applied` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M3_digest_drops_where` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M5_digest_drops_export` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-c.C6_gate_manifest_bytes` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-c.C7_digest_handed_to_engine` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 255 | 1 | killed |
| `u77-c.C8_unfiled_rows_warned` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 255 | 2 | killed |
| `r1264.M22_readable_dates` | `src/cratekit/intake/cli.py` | user | 4 file(s) | 182 | 6 | killed |
| `r1295.M16_set_aside_one_word` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 221 | 4 | killed |
| `r290-author.S05_intake_call_removed` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 126 | 11 | killed |
| `r431-b.B10_an_older_payload_reads_as_solo` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 1 | killed |
| `r431-b.B9_the_freeze_drops_the_field` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 3 | killed |
| `r504-b.B1_verb_drops_short` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 3 | killed |
| `r504-b.B4_no_progress_block` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 5 | killed |
| `r504-b.B6_warning_reworded` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 3 | killed |
| `r515-operator.S11_intake_playlist_no_warning` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 4 | killed |
| `r679-b.D1_intake_gate_on_question_alone` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 830 | 2 | killed |
| `r682-a.M1_no_by_reason_in_summary` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 122 | 4 | killed |
| `r682-a.M2_non_string_why_counted` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r682-a.M3_empty_why_counted` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r682-a.M4_state_keys_not_seeded` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 3 | killed |
| `r682-a.M5_reason_counted_twice` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 4 | killed |
| `r682-a.M6_reason_counted_outside_state_guard` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r706-c.C1_parts_note_never_said` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `r706-c.C3_summary_ignores_the_payload` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r924.C1_set_identify_not_told` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 119 | 4 | killed |
| `r924.C3_recording_drops_progress` | `src/cratekit/intake/cli_identify.py` | user | 3 file(s) | 119 | 2 | killed |
| `r925.S1_no_folder_check` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 108 | 40 | killed |
| `r925.S2_out_ignored` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r925.S3_no_write` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 3 | killed |
| `r925.S4_write_failure_refuses` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u103-b.C14_offered_under_its_own_key` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 595 | 1 | killed |
| `u103-b.C3_out_must_be_a_folder` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 595 | 1 | killed |
| `u103-b.C6_served_note` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 595 | 1 | killed |
| `u103-b.C7_unwritten_note` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 595 | 1 | killed |
| `u103-b.C8_set_no_op_carries_warnings` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 2 | killed |
| `u103-b.C9_refusal_counts_the_gap` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 595 | 1 | killed |
| `u104-d.C2_refusal_named_for_the_address` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-d.C3_detail_renamed` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-d.C4_scratch_left_said` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-d.C5_no_digest_token_is_the_address` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-e.E2_timeout_is_retryable` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-e.E3_honest_zero_names_the_address` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 108 | 1 | killed |
| `u104-e.E4_identify_library_before_fetch` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 2 | killed |
| `u113-a.A7_payload_drops_name` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 42 | 32 | killed |
| `u120.L1_date_frozen_when_none` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u120.L2_date_added_ignored` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u129-author.A3_abort_still_writes` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 20 | 1 | killed |
| `u213.M11_unreadable_said_isrc` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u213.M12_absent_rule` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 1 | killed |
| `u213.M13_unidentified_any` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u213.M6_readable_refuses_nameless` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u213.M8_readable_unread_excludes_read` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 1 | killed |
| `u213.M9_readable_order_holds_unread` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u249.M21_intake_reset_leaves_reader` | `src/cratekit/intake/cli.py` | maintainer | 3 file(s) | 128 | 1 | killed |
| `u57-recognition-and-items.C3_missing_ref_not_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 2 | killed |
| `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u57-recognition-and-items.C7_foreign_job_driven` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u70.E1_missing_id_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 2 | killed |
| `u70.S2_sentinel_casefold` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 241 | 2 | killed |
| `u70.S3_sentinel_strip` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 241 | 1 | killed |
| `u70.S4_canonical_source` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 241 | 2 | killed |
| `u70.S5_source_id_recorded` | `src/cratekit/intake/cli.py` | maintainer | 2 file(s) | 241 | 1 | killed |
| `u70.S6_source_id_only_for_hearts` | `src/cratekit/intake/cli.py` | maintainer | 2 file(s) | 241 | 1 | killed |
| `r675.G10_repair_apply_asks_with_no_candidates` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 120 | 1 | killed |
| `r675.G9_repair_plan_asks_with_no_candidates` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 120 | 1 | killed |
| `u102-a.P1_root_boundary` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.P2_root_casefold` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.P3_root_filter` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.P4_unchanged` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.P5_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-a.P6_missing_says_what_exists` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U1_no_stored_path` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U2_bare_filename` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-a.U3_empty_name` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U4_same_suffix` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U5_linked_file` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G1_plan_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G2_post_gate_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G4_plan_collisions` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-b.G5_claim` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G6_abort` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G7_referenced_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G8_collision_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-b.G9_post_gate_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.R1_retryable_seed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-b.R2_retryable_after_gate` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.S1_stub_removed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u169.N5_repair_scan_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 37 | 2 | killed |
| `u169.N6_repair_apply_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 37 | 1 | killed |
| `r1709.M23_intake_exact_by_token` | `src/cratekit/intake/candidates.py` | user | 29 file(s) | 3824 | 2 | killed |
| `r879-a.C10_offset_counts_pages_not_rows` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 4 | killed |
| `r879-a.C11_sole_exact_ignores_full` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 106 | 4 | killed |
| `r879-a.C1_full_reads_total_not_last_page` | `src/cratekit/intake/candidates.py` | user | 2 file(s) | 106 | 5 | killed |
| `r879-a.C2_walk_ignores_short_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 6 | killed |
| `r879-a.C3_settled_early_without_ambiguity` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 2 | killed |
| `r879-a.C4_settled_early_without_unreadable` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-a.C6_settled_early_without_several` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-a.C7_bound_off_by_one` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `r879-a.C9_read_pages_forgets_last_page` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 5 | killed |
| `r879-b.C5r_settled_early_without_unnamed_exact` | `src/cratekit/intake/candidates.py` | maintainer | 1 file(s) | 56 | 1 | killed |
| `r879-b.C8r_ceiling_coefficient` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-a.A1_ambiguous_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-a.A2_full_page_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-a.A3_unreadable_ignored` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-a.A4_no_identifier_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-a.A5_two_exact_picked` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 3 | killed |
| `u79-b.B1_floor_halved` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B2_score_before_exact` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B3_no_identifier_offered` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-b.B4_rejected_read_as_accepted` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B5_unspecific_yes_takes_first` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B6_option_track_mismatch` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B8_open_item_searched_again` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `r1255.F1_refill_plan_unlisted` | `src/cratekit/intake/refill.py` | user | 2 file(s) | 28 | 1 | killed |
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
| `u175.F3_analyze_asked` | `src/cratekit/intake/refill.py` | user | 2 file(s) | 27 | 1 | killed |
| `u175.F4_bridge_names_any_state` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `u175.F5_bridge_names_by_id_order` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 13 | 1 | killed |
| `r501-c.M1_export_name_check` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-c.M2_export_identity_check` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-c.M3_missing_is_not_imported` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 4 | killed |
| `r501-c.M4_nothing_recorded` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-c.M5_retire_name_guard` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-c.M6_retire_link_guard` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-d.M10_waiting_legacy` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-d.M11_close_refusal_reported` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-d.M13_waiting_needs_export` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-d.M7_retire_next_free_name` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r501-d.M9_waiting_capture` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1058 | 1 | killed |
| `r773-b.P1_proof_granted_whatever_the_export_names` | `src/cratekit/intake/imported_cli.py` | user | 2 file(s) | 131 | 6 | killed |
| `r1499.B01_pass_suffix` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.B02_pass_handler` | `src/cratekit/intake/beside.py` | maintainer | 6 file(s) | 324 | 2 | killed |
| `r1499.B03_pass_step` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 6 | killed |
| `r1499.B04_pass_maybe_renamed` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.B05_arrived_items` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 4 | killed |
| `r1499.B06_arrived_count` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.B08_kept_identity` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 5 | killed |
| `r1499.B09_unlistable` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.B10_plain_step_moves_out` | `src/cratekit/intake/beside.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1255.R3_rotation_warning_gate` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 72 | 3 | killed |
| `r1255.R4_rotation_warning_wording` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 72 | 2 | killed |
| `u111-d.D1_empty_plan_asks` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 1027 | 4 | killed |
| `u111-d.D2_ack_before_gate` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 1027 | 1 | killed |
| `u267.M11_rotation_opens_its_own` | `src/cratekit/intake/rotate_cli.py` | user | 2 file(s) | 45 | 4 | killed |
| `r301.R1_seam_falls_back_to_defaults` | `src/cratekit/intake/recognize.py` | user | 3 file(s) | 183 | 1 | killed |
| `r924.R1_bound_identifier_not_told` | `src/cratekit/intake/recognize.py` | user | 2 file(s) | 78 | 4 | killed |
| `u37-author-light.G2_recognition_gate` | `src/cratekit/intake/recognize.py` | user | 1 file(s) | 8 | 1 | killed |
| `u121-b.S25r_bridge_backfill` | `src/cratekit/intake/inspiration_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S24_ack_before_gate` | `src/cratekit/intake/inspiration_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r770-b.B2_gate_asked_before_the_acknowledgment` | `src/cratekit/intake/land_native.py` | user | 2 file(s) | 77 | 2 | killed |
| `u188.M13_fields_repeated` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u319.M8_ok_on_any_field` | `src/cratekit/intake/land_native.py` | user | 3 file(s) | 89 | 2 | killed |
| `r925.S5_unwritten_note_names_no_job_show` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u103-b.C10_open_question_is_pending` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 595 | 1 | killed |

## Row definitions

### `r1467.M19_root_unreadable_refuses`

pass_landed: read a library root that cannot be read as a pass that never landed

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M19_root_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_an_unreadable_library_root_refuses_rather_than_read_the_pass_as_landed`

Old text:

```
    except OSError as exc:
        raise refuse(
            "library-root-unreachable",
```

New text:

```
    except OSError as exc:
        return False
        raise refuse(
            "library-root-unreachable",
```

### `r1467.M20_retired_file_proves`

pass_landed: read only a pending intake file, so a retired one proves nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M20_retired_file_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_retired_intake_file_proves_the_pass`

Old text:

```
            if unretired_name(entry.name) == wanted and entry.is_file():
```

New text:

```
            if entry.name == wanted and entry.is_file():
```

### `r1467.M21_native_record_proves`

pass_landed: never read the native landing's record

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M21_native_record_proves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_track_no_download_names_refuses_the_fresh_go_and_only_an_unproven_go_is_named[native]`

Old text:

```
    return bool(native.landings_of_pass(cfg, name))
```

New text:

```
    return False
```

### `r1467.M22_proof_is_a_file`

pass_landed: a directory named as the intake file proves the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M22_proof_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_proof_of_another_pass_proves_nothing`

Old text:

```
            if unretired_name(entry.name) == wanted and entry.is_file():
```

New text:

```
            if unretired_name(entry.name) == wanted:
```

### `r1677.L1_rehearsal_unmeasured`

land_cli: the rehearsal's own check is not measured before its copy

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L1_rehearsal_unmeasured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`

Old text:

```
    snapshot.assert_room_for_check(area.database)
    try:
```

New text:

```
    try:
```

### `r1677.L2_rehearsal_room_silent`

land_cli: a rehearsal check whose copy found no room is told as a failed integrity check

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1677.json`, row `L2_rehearsal_room_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_sync_mark.py`
- Collected: 130 against a baseline of 130
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
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
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
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
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
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
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
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
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
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
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
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
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

### `r770-b.B3_an_abort_writes`

ask_then_write: write whatever the answer was

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B3_an_abort_writes`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
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

### `u110-b.B1_pass_names_file`

--pass no longer names the intake file, so sync mark cannot find the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B1_pass_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
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
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land.py`
- Collected: 53 against a baseline of 53
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

### `u121-b.S20r_bridge_set`

intake_land: --set on a bridge tree is not refused, the batch lands with no playlist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u121-b.json`, row `S20r_bridge_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_on_the_bridge_given_set_is_refused_by_name_before_anything_moves`

Old text:

```
    if ctx.args.set_job:
        set_playlist.assert_native(medium, landing=True)
```

New text:

```
    if False:
        set_playlist.assert_native(medium, landing=True)
```

### `u126.P3_gate_fact`

Rename the content link fact on the gate screen, so the value and its count are not where the person reads them

- File: `src/cratekit/intake/land_native.py`
- Source: `u126.json`, row `P3_gate_fact`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 438 against a baseline of 438
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
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
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
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
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
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
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

### `u127.L6_bridge_ignores_calibration`

The bridge names the vocals verb as owed on an uncalibrated library

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L6_bridge_ignores_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
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

### `u127.L7_land_warnings_unsaid`

intake land gives no vox warning

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L7_land_warnings_unsaid`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_unreadable]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    warnings.extend(vox_warnings(landed.collection))
```

New text:

```
    warnings.extend([])
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

### `u129-author.A19_plan_archive_always_none`

A set landing never plans the account archive

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A19_plan_archive_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None

```

New text:

```
    return None

```

### `u129-author.A4_archive_raise_fails_landing`

Let an account archive raise escape the landing write after rows are in the library

- File: `src/cratekit/intake/land_native.py`
- Source: `u129-author.json`, row `A4_archive_raise_fails_landing`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning[transient]`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:
        message = (
            exc.cause.message if isinstance(exc, CratekitError) else f"{type(exc).__name__}: {exc}"
        )
        return [
            {
                "code": LAND_ARCHIVE_FAILED,
                "message": (
                    f"the account archive could not finish after the landing wrote "
                    f"({message}); the batch is in the library, run crate export "
                    f"archive over the set once the account can be reached"
                ),
            }
        ]
    return list(warnings)

```

New text:

```
    _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    return list(warnings)

```

### `u129-author.A5_archive_return_discarded`

Discard apply_archive warnings so a not-renamed return is silent on the landed envelope

- File: `src/cratekit/intake/land_native.py`
- Source: `u129-author.json`, row `A5_archive_return_discarded`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_u129_set_account_playlist.py::test_landing_archive_failure_after_write_is_a_warning[changed]`

Old text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
    except Exception as exc:

```

New text:

```
    try:
        _data, warnings, _wrote = set_cli.apply_archive(cfg, archived)
        warnings = []
    except Exception as exc:

```

### `u135.A3_found_vs_made_collapsed`

The gate screen always says found-or-made when no recorded INBOX playlist is named

- File: `src/cratekit/intake/land_native.py`
- Source: `u135.json`, row `A3_found_vs_made_collapsed`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`, `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 9 against a baseline of 9
- Kills: 6 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_recorded_inbox_playlist_removed_before_the_next_landing_is_not_joined`
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
        if rows.batch_playlist_id:
            facts["inbox"] = (
                f"adds to the playlist an earlier landing of this set made "
                f"(row {rows.batch_playlist_id})"
            )
        elif rows.inbox_found_by_name:
            facts["inbox"] = "found live by name, not recorded"
        else:
            facts["inbox"] = "made"

```

New text:

```
        facts["inbox"] = (
            f"adds to the playlist an earlier landing of this set made "
            f"(row {rows.batch_playlist_id})"
            if rows.batch_playlist_id
            else "found live by its name under INBOX, or made"
        )

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

### `u146-c.L3_gate_asked_for_nothing`

_place_owned: a pass whose owned hearts are all placed opens the database to write and asks the gate over nothing

- File: `src/cratekit/intake/land_native.py`
- Source: `u146-c.json`, row `L3_gate_asked_for_nothing`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
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
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 25 against a baseline of 25
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
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
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

### `u156.L23_label_beside_manifest`

_label_flag: accept --label beside --manifest, so one of two answers silently wins

- File: `src/cratekit/intake/land_cli.py`
- Source: `u156.json`, row `L23_label_beside_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 90 against a baseline of 90
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
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land.py`
- Collected: 117 against a baseline of 117
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

### `u157.L1_selection_counts`

awaiting_analysis: count no row as carrying dyn

- File: `src/cratekit/intake/land_native.py`
- Source: `u157.json`, row `L1_selection_counts`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
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
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 126 against a baseline of 126
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
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
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

### `u162.L10_interrupt_cancel`

_rehearse_native: an interrupt reported as internal-error rather than cancelled

- File: `src/cratekit/intake/land_cli.py`
- Source: `u162.json`, row `L10_interrupt_cancel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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

### `u165.L1_bridge_skip`

_land_native: predict a filing on a routing tree still on the bridge

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L1_bridge_skip`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 135 against a baseline of 135
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
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 135 against a baseline of 135
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

### `u165.L3_filing_tail`

_land_native: never file after the landing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L3_filing_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 135 against a baseline of 135
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

### `u165.L4_files_into`

_native_payload: drop each item's files into

- File: `src/cratekit/intake/land_native.py`
- Source: `u165.json`, row `L4_files_into`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 135 against a baseline of 135
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
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
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

### `u188.M1_stored_pair_dropped`

_mapped_back: leave the stored spelling pair out, so FolderPath on a renamed drive is never mapped back (the defect)

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M1_stored_pair_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
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

### `u319.M9_warning_drops_the_short_path`

land_cli: the awaiting analysis warning names one path again

- File: `src/cratekit/intake/land_native.py`
- Source: `u319.json`, row `M9_warning_drops_the_short_path`
- Moved: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_intake_land_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_the_warning_names_and_counts_each_selection`

Old text:

```
                f"for analysis, and {selections}; {AUTO_ANALYSIS_STEP}; then "
```

New text:

```
                f"for analysis, and {selections}; then "
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
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
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
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
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
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 255 against a baseline of 255
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

### `r1264.M22_readable_dates`

list_playlist_readable: give no added dates, so a pair's later change calls read every time as unknown

- File: `src/cratekit/intake/cli.py`
- Source: `r1264.json`, row `M22_readable_dates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_merge.py`
- Collected: 182 against a baseline of 182
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_back.py::test_the_snapshot_records_each_account_tracks_added_date`

Old text:

```
        dates=_added_dates(rows, tracks),
```

New text:

```
        dates={},
```

### `r1295.M16_set_aside_one_word`

set_aside: always names the title as the absent half, so an artistless track is misnamed

- File: `src/cratekit/intake/cli.py`
- Source: `r1295.json`, row `M16_set_aside_one_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/intake/test_workers.py`, `tests/test_sync_all.py`
- Collected: 221 against a baseline of 221
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
why=f"the account lists it with no {_absent(title)}"
```

New text:

```
why="the account lists it with no title"
```

### `r290-author.S05_intake_call_removed`

Remove the one jobs.raise_for_state call from intake/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/intake/cli.py`
- Source: `r290-author.json`, row `S05_intake_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r431-b.B10_an_older_payload_reads_as_solo`

A payload frozen before the field existed thaws as billing one artist and asks for a companion

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B10_an_older_payload_reads_as_solo`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`

Old text:

```
        several_artists=bool(said.get("several_artists", True)),
```

New text:

```
        several_artists=bool(said.get("several_artists", False)),
```

### `r431-b.B9_the_freeze_drops_the_field`

The intake freeze stops carrying several_artists, so the worker resolves from a track that never looked

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B9_the_freeze_drops_the_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
        "several_artists": row.several_artists,
```

New text:

```
(empty)
```

### `r504-b.B1_verb_drops_short`

intake playlist favorites lists the hearts and throws the shortfall away

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B1_verb_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
            tracks, short = list_favorites(found)
```

New text:

```
            tracks, short = list_favorites(found)[0], None
```

### `r504-b.B4_no_progress_block`

The verb carries no shortfall block under progress

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B4_no_progress_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
        extra = {"shortfall": short.block()} if short is not None else {}
```

New text:

```
        extra = {}
```

### `r504-b.B6_warning_reworded`

The warning names no numbers

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B6_warning_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
            f"the account's hearts listed short: {short.summary()}. The provider "
```

New text:

```
            f"the account's hearts listed short. The provider "
```

### `r515-operator.S11_intake_playlist_no_warning`

An intake playlist listed short carries no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S11_intake_playlist_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        warnings = (warned(short),) if short is not None else ()
```

New text:

```
        warnings = ()
```

### `r679-b.D1_intake_gate_on_question_alone`

intake worker: gate the store on the needs-review state alone, the code before the fix round

- File: `src/cratekit/intake/cli.py`
- Source: `r679-b.json`, row `D1_intake_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 830 against a baseline of 830
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if not match_cli.touches_the_queue(found):
```

New text:

```
    if found.state is not match.MatchState.NEEDS_REVIEW:
```

### `r682-a.M1_no_by_reason_in_summary`

the intake summary no longer carries by_reason, so the json and the rendering both lose the breakdown

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M1_no_by_reason_in_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_render_payloads.py`
- Collected: 122 against a baseline of 122
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`

Old text:

```
        "by_reason": by_reason,

```

New text:

```
(empty)
```

### `r682-a.M2_non_string_why_counted`

a why that is not a string is counted under its own value as a slug

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M2_non_string_why_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
            if isinstance(why, str) and why:
```

New text:

```
            if why:
```

### `r682-a.M3_empty_why_counted`

an empty why is counted under the empty string as a reason

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M3_empty_why_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
            if isinstance(why, str) and why:
```

New text:

```
            if isinstance(why, str):
```

### `r682-a.M4_state_keys_not_seeded`

by_reason carries only the states some row reached, so suppressed with no rows is absent rather than an empty mapping

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M4_state_keys_not_seeded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
        "by_reason": by_reason,

```

New text:

```
        "by_reason": {word: reasons for word, reasons in by_reason.items() if reasons},

```

### `r682-a.M5_reason_counted_twice`

each row adds two to its reason, a realistic nearby coefficient

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M5_reason_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`

Old text:

```
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
```

New text:

```
                by_reason[word][why] = by_reason[word].get(why, 0) + 2
```

### `r682-a.M6_reason_counted_outside_state_guard`

a reason is counted before the state word is checked, so a row in a state the counts do not know is counted under it

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M6_reason_counted_outside_state_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
        if word in counts:
            counts[word] += 1
            why = report.get("why")
            if isinstance(why, str) and why:
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
```

New text:

```
        why = report.get("why")
        if isinstance(why, str) and why:
            by_reason.setdefault(word, {})[why] = by_reason.get(word, {}).get(why, 0) + 1
        if word in counts:
            counts[word] += 1
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

### `r706-c.C3_summary_ignores_the_payload`

The resume summary reports one part rather than reading the frozen count

- File: `src/cratekit/intake/cli.py`
- Source: `r706-c.json`, row `C3_summary_ignores_the_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
        "parts": int(payload.get(PARTS) or 1),
```

New text:

```
        "parts": 1,
```

### `r924.C1_set_identify_not_told`

intake set does not hand its progress to identification

- File: `src/cratekit/intake/cli.py`
- Source: `r924.json`, row `C1_set_identify_not_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
            result = pipeline.identify_only(
                held.path,
                refresh=bool(ctx.args.refresh),
                recognition=cfg.recognition,
                progress=ctx.progress,
            )
```

New text:

```
            result = pipeline.identify_only(
                held.path,
                refresh=bool(ctx.args.refresh),
                recognition=cfg.recognition,
            )
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

### `r925.S1_no_folder_check`

intake set skips the free tracklist folder check, so a folder that is a file is found only after the spend

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S1_no_folder_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/intake/test_set_fetch.py`
- Collected: 108 against a baseline of 108
- Kills: 40 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[failed]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[several]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[timed-out]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[not-there]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[outside]`
  - `tests/intake/test_set_fetch.py::test_a_local_path_never_consults_the_fetch_seam`
  - `tests/intake/test_set_fetch.py::test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint`
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_made_is_a_fact_about_this_machine`
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`
  - `tests/intake/test_set_fetch.py::test_a_scratch_root_inside_the_library_refuses_before_anything_is_fetched`
  - `tests/intake/test_set_fetch.py::test_identification_that_raises_still_removes_the_fetched_mix`
  - `tests/intake/test_set_fetch.py::test_the_page_a_mix_came_from_is_frozen_on_the_set_job`
  - ... and 25 more, see the JSON sidecar

Old text:

```
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
```

New text:

```
        out = Path(ctx.args.out or cfg.paths.download_staging / TRACKLISTS_DIR)
```

### `r925.S2_out_ignored`

intake set ignores --out and always writes under download staging

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S2_out_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`

Old text:

```
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
```

New text:

```
        out = _tracklist_dir(cfg, None, local if local is not None else source.strip())
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

### `u103-b.C14_offered_under_its_own_key`

Offer identify's version questions under the match verb's key instead of its own

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C14_offered_under_its_own_key`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
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
- Collected: 595 against a baseline of 595
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
- Collected: 595 against a baseline of 595
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
- Collected: 595 against a baseline of 595
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

### `u103-b.C8_set_no_op_carries_warnings`

Drop the warnings from intake set's nothing identified envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u103-b.json`, row `C8_set_no_op_carries_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                outcome=Outcome.NO_OP,
            )
```

### `u103-b.C9_refusal_counts_the_gap`

Let the unwritable tracklist refusal promise a free rerun over chunks that got no answer

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C9_refusal_counts_the_gap`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
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
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
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

### `u104-e.E3_honest_zero_names_the_address`

Report the scratch file's path as the source of a mix nobody recognised

- File: `src/cratekit/intake/cli.py`
- Source: `u104-e.json`, row `E3_honest_zero_names_the_address`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`

Old text:

```
                    chunks=result.chunks,
                    source=held.ref,
```

New text:

```
                    chunks=result.chunks,
                    source=str(held.path),
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

### `u113-a.A7_payload_drops_name`

queue_playlist is handed the name and records nothing

- File: `src/cratekit/intake/cli.py`
- Source: `u113-a.json`, row `A7_payload_drops_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 42 against a baseline of 42
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_a_name_the_export_came_to_hold_after_the_gate_is_refused_and_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_a_rerun_of_the_same_pass_is_a_no_op`
  - `tests/test_intake_land_account_playlists.py::test_a_row_that_only_resembles_a_file_does_not_claim_it`
  - `tests/test_intake_land_account_playlists.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_an_answer_given_for_one_split_is_stale_for_another`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_sync_all_records_the_name_the_account_listed_on_each_playlist_job`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    if name:
        payload[PLAYLIST_NAME] = name
```

New text:

```
    if name and False:
        payload[PLAYLIST_NAME] = name
```

### `u120.L1_date_frozen_when_none`

list_favorites: a heart with no date is frozen with no key, as an older build did

- File: `src/cratekit/intake/cli.py`
- Source: `u120.json`, row `L1_date_frozen_when_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`

Old text:

```
        if key in frozen and HEARTED not in frozen[key]:
            frozen[key][HEARTED] = hearted_on(row)
```

New text:

```
        if key in frozen and HEARTED not in frozen[key] and hearted_on(row):
            frozen[key][HEARTED] = hearted_on(row)
```

### `u120.L2_date_added_ignored`

hearted_on: the older client's date_added is not read

- File: `src/cratekit/intake/cli.py`
- Source: `u120.json`, row `L2_date_added_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`

Old text:

```
    for name in ("user_date_added", "date_added"):
```

New text:

```
    for name in ("user_date_added",):
```

### `u129-author.A3_abort_still_writes`

Apply the account playlist even when the gate said abort

- File: `src/cratekit/intake/cli.py`
- Source: `u129-author.json`, row `A3_abort_still_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist`

Old text:

```
    if option != "apply" or not built.writes:
        return notes, built.payload

```

New text:

```
    if not built.writes:
        return notes, built.payload

```

### `u213.M11_unreadable_said_isrc`

Unreadable.said: name the track with no ISRC, so the backfill cannot find it by its code

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M11_unreadable_said_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        return {"artist": self.artist, "title": self.title, "isrc": self.isrc}
```

New text:

```
        return {"artist": self.artist, "title": self.title, "isrc": ""}
```

### `u213.M12_absent_rule`

_absent: name the missing half by the artist alone, the rule the review replaced, so a row with neither says no artist

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M12_absent_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_aside_track_names_the_half_the_reader_names`

Old text:

```
    return "artist" if match.split_title(title)[0] else "title"
```

New text:

```
    return "artist" if title else "title"
```

### `u213.M13_unidentified_any`

_refuse_unidentified: refuse only when more than one row carries no id

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M13_unidentified_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_listing_that_fails_refuses_and_queues_nothing[no-id-by-position]`
  - `tests/intake/test_workers.py::test_a_row_the_reader_refuses_refuses_the_playlist_and_queues_nothing[no-identifier-by-position]`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    if missing:
        raise _unusable(
```

New text:

```
    if len(missing) > 1:
        raise _unusable(
```

### `u213.M6_readable_refuses_nameless`

list_playlist_readable: drop the refusal of a row carrying no provider id, so it is silently dropped from the listing

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M6_readable_refuses_nameless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    _refuse_unidentified(nameless)
    tracks = frozen_rows(tuple(read))
```

New text:

```
    tracks = frozen_rows(tuple(read))
```

### `u213.M8_readable_unread_excludes_read`

list_playlist_readable: keep a track as unread even when another row of it read

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M8_readable_unread_excludes_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`

Old text:

```
    unread = {ref: one for ref, one in refused.items() if ref not in tracks}
```

New text:

```
    unread = dict(refused)
```

### `u213.M9_readable_order_holds_unread`

list_playlist_readable: order only the tracks that read, so a twin's snapshot drops the unread track

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M9_readable_order_holds_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        order.setdefault(ref, None)
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
```

New text:

```
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
            order.setdefault(ref, None)
```

### `u249.M21_intake_reset_leaves_reader`

intake.cli.reset_cache: clear the drive's view and leave the reader's memory

- File: `src/cratekit/intake/cli.py`
- Source: `u249.json`, row `M21_intake_reset_leaves_reader`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_sync_unmark.py`, `tests/intake/test_workers.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`

Old text:

```
    _RESOLVED.clear()
    match.reset_cache()
```

New text:

```
    _RESOLVED.clear()
```

### `u57-recognition-and-items.C3_missing_ref_not_refused`

A provider row without an identifier is queued rather than refused by position

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C3_missing_ref_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_listing_that_fails_refuses_and_queues_nothing[no-id-by-position]`
  - `tests/intake/test_workers.py::test_a_row_the_reader_refuses_refuses_the_playlist_and_queues_nothing[no-identifier-by-position]`

Old text:

```
        if row.origin != match.TEXT and not row.ref
```

New text:

```
        if False
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

### `u57-recognition-and-items.C7_foreign_job_driven`

A job of another verb is driven under this verb's envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C7_foreign_job_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_job_of_another_handler_lists_no_tracks_and_is_not_driven_under_this_envelope`

Old text:

```
    if job.handler_key not in INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u70.E1_missing_id_refused`

Existing: a provider row with no id is not refused by position, so a heart without one is queued under a blank key

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `E1_missing_id_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_listing_that_fails_refuses_and_queues_nothing[no-id-by-position]`
  - `tests/intake/test_workers.py::test_a_row_the_reader_refuses_refuses_the_playlist_and_queues_nothing[no-identifier-by-position]`

Old text:

```
        if row.origin != match.TEXT and not row.ref
```

New text:

```
        if row.origin != match.TEXT and False
```

### `u70.S2_sentinel_casefold`

The sentinel is compared case sensitively, so Favorites is read as a playlist reference

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S2_sentinel_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[Favorites]`

Old text:

```
    return str(reference or "").strip().casefold() == FAVORITES
```

New text:

```
    return str(reference or "").strip() == FAVORITES
```

### `u70.S3_sentinel_strip`

The sentinel is compared unstripped, so a padded favorites is read as a playlist reference

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S3_sentinel_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`

Old text:

```
    return str(reference or "").strip().casefold() == FAVORITES
```

New text:

```
    return str(reference or "").casefold() == FAVORITES
```

### `u70.S4_canonical_source`

The job records the reference as typed rather than the canonical favorites, so the resume argv carries the typed spelling

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S4_canonical_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[Favorites]`

Old text:

```
        if hearts:
            reference = FAVORITES
        found = catalogue.resolve(cfg)
```

New text:

```
        found = catalogue.resolve(cfg)
```

### `u70.S5_source_id_recorded`

A hearts job is queued with no source_id, so nothing can tell it from a playlist job

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S5_source_id_recorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`

Old text:

```
            source_id=FAVORITES_SOURCE_ID if hearts else None,
```

New text:

```
            source_id=None,
```

### `u70.S6_source_id_only_for_hearts`

Every playlist job is stamped source_id favorites, so a playlist reads as the hearts listing

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S6_source_id_only_for_hearts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_playlist_reference_still_reaches_the_playlist_and_not_the_hearts`

Old text:

```
            source_id=FAVORITES_SOURCE_ID if hearts else None,
```

New text:

```
            source_id=FAVORITES_SOURCE_ID,
```

### `r675.G10_repair_apply_asks_with_no_candidates`

repair_cli apply: the repair verb's read after the gate hands the guard no candidates

- File: `src/cratekit/intake/repair_cli.py`
- Source: `r675.json`, row `G10_repair_apply_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 120 against a baseline of 120
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`

Old text:

```
        naming_cli.referenced_keys(cfg, renaming=[Path(item["path"]) for item in renames])
```

New text:

```
        naming_cli.referenced_keys(cfg, renaming=[])
```

### `r675.G9_repair_plan_asks_with_no_candidates`

repair_cli plan: the repair verb's plan read hands the guard no candidates

- File: `src/cratekit/intake/repair_cli.py`
- Source: `r675.json`, row `G9_repair_plan_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 120 against a baseline of 120
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`

Old text:

```
        naming_cli.referenced_keys(cfg, renaming=[path for _, path in candidates])
```

New text:

```
        naming_cli.referenced_keys(cfg, renaming=[])
```

### `u102-a.P1_root_boundary`

_under: match the root as a bare prefix, without the separator, so a sibling folder sharing the prefix is inside it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P1_root_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder`

Old text:

```
    return held == wanted or held.startswith(wanted + "/")
```

New text:

```
    return held == wanted or held.startswith(wanted)
```

### `u102-a.P2_root_casefold`

_key: compare the root exactly instead of casefolded

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P2_root_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return locations.norm_for_compare(path)
```

### `u102-a.P3_root_filter`

_plan_for: ignore the root, so an accepted item outside it is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P3_root_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder`

Old text:

```
        if accepted.path is not None and not _under(accepted.path, root):
```

New text:

```
        if False:
```

### `u102-a.P4_unchanged`

_plan_for: stop setting aside a proposal that names the file's own name, so it is planned as a rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P4_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_that_asked_for_no_change_is_listed_with_its_reason`

Old text:

```
        if path.name == accepted.proposed:
```

New text:

```
        if False:
```

### `u102-a.P5_missing`

_plan_for: stop setting aside an accepted item whose file is gone, so the run after an apply plans it again

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P5_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`
  - `tests/intake/test_repair_apply.py::test_an_accepted_proposal_is_shown_asked_renamed_and_then_converges`

Old text:

```
        if not path.is_file():
            # ONE CLASS
```

New text:

```
        if False:
            # ONE CLASS
```

### `u102-a.P6_missing_says_what_exists`

_plan_for: always word a missing file as a rename already carried out, whether or not any file carries the proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P6_missing_says_what_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`

Old text:

```
            if target.is_file():
                why = (
```

New text:

```
            if True:
                why = (
```

### `u102-a.U1_no_stored_path`

_unusable_why: drop the refusal over an item the queue holds no path for

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U1_no_stored_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
    if accepted.path is None:
        return (
```

New text:

```
    if False:
        return (
```

### `u102-a.U2_bare_filename`

_unusable_why: stop requiring the proposed name to be a bare filename, so a path with a separator is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U2_bare_filename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[../escaped.flac-not a bare filename]`
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[nested/inside.flac-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if not proposed or proposed in {".", ".."}:
```

### `u102-a.U3_empty_name`

_unusable_why: stop refusing an empty proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U3_empty_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if proposed in {".", ".."} or Path(proposed).name != proposed:
```

### `u102-a.U4_same_suffix`

_unusable_why: drop the check that the proposed name keeps the file's extension

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U4_same_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[04A - 124 - Song - Artist.txt-change the file's extension]`

Old text:

```
    if Path(proposed).suffix.lower() != Path(accepted.path).suffix.lower():
```

New text:

```
    if False:
```

### `u102-a.U5_linked_file`

_unusable_why: drop the check that the stored path names the file the proposal was shown for, so a link's target is renamed

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U5_linked_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_linked_file_is_never_renamed_through_its_link`

Old text:

```
    if accepted.recorded and Path(accepted.path).name != accepted.recorded:
```

New text:

```
    if False:
```

### `u102-b.G1_plan_referenced`

_plan_for: treat no candidate as referenced, leaving only the post gate check to hold the file

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G1_plan_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
        if not naming_cli.is_referenced(path, referenced)
    ]
```

New text:

```
        if True
    ]
```

### `u102-b.G2_post_gate_referenced`

_apply: drop the referenced check made after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G2_post_gate_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_row_after_the_gate_holds_the_file_and_an_unreadable_collection_refuses`

Old text:

```
        if naming_cli.is_referenced(path, referenced):
            _owed(
```

New text:

```
        if False:
            _owed(
```

### `u102-b.G4_plan_collisions`

_plan_for: detect no collision while the plan is built, leaving it to the claim

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G4_plan_collisions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
    collides = naming_cli.held_collisions([(path, acc.proposed) for acc, path in free])
```

New text:

```
    collides: dict[str, str] = {}
```

### `u102-b.G5_claim`

_apply: skip the atomic claim, so a name taken after the gate is overwritten by the rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G5_claim`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_name_refused_or_taken_after_the_gate_is_named_and_never_overwritten`

Old text:

```
            claimed = naming.claim_target(target)
```

New text:

```
            claimed = True
```

### `u102-b.G6_abort`

_apply: carry on past an abort answer

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G6_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_proposal_is_shown_asked_renamed_and_then_converges`

Old text:

```
    if option == "abort":
```

New text:

```
    if False:
```

### `u102-b.G7_referenced_is_owed`

_HELD: stop counting a referenced file as an accepted rename that did not happen, so the run answers ok over it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G7_referenced_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (COLLIDES, UNUSABLE)
```

### `u102-b.G8_collision_is_owed`

_HELD: stop counting a collision as owed, which is R-172 itself, a skipped collision reported as ok

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G8_collision_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (REFERENCED, UNUSABLE)
```

### `u102-b.G9_post_gate_missing`

_apply: drop the check that the file is still there after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G9_post_gate_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_file_deleted_after_the_gate_is_named_and_not_called_renamed`

Old text:

```
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
```

New text:

```
(empty)
```

### `u102-b.R1_retryable_seed`

_apply: call a run retryable when all it holds is a file only a person can release

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R1_retryable_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
        item["action"] in _HELD and item["action"] not in _NEEDS_A_PERSON
```

New text:

```
        item["action"] in _HELD
```

### `u102-b.R2_retryable_after_gate`

_owed: stop marking the run retryable when a rename fails after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R2_retryable_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_interrupt_or_a_refused_rename_after_the_claim_leaves_no_stub`

Old text:

```
        nonlocal retryable
        retryable = True
```

New text:

```
        nonlocal retryable
```

### `u102-b.S1_stub_removed`

_apply: leave the zero byte claim behind when the rename did not happen

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `S1_stub_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_interrupt_or_a_refused_rename_after_the_claim_leaves_no_stub`

Old text:

```
            if not moved:
                target.unlink(missing_ok=True)
```

New text:

```
            if not moved:
                pass
```

### `u169.N5_repair_scan_bypasses`

repair paths: read --root as the base did, bypassing the helper

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u169.json`, row `N5_repair_scan_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/intake/test_repair_apply.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_repair_paths_refuses_a_root_with_no_folder`
  - `tests/test_root_option.py::test_repair_paths_scans_a_relative_root_inside_the_library`

Old text:

```
    root = naming_cli.root_folder(ctx.args.root, cfg, verb="repair paths")
```

New text:

```
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
```

### `u169.N6_repair_apply_bypasses`

repair paths --apply: take a relative root as it is

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u169.json`, row `N6_repair_apply_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/intake/test_repair_apply.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_root_option.py::test_repair_apply_reads_a_relative_root_against_the_library_root`

Old text:

```
        naming_cli.root_path(ctx.args.root, cfg, verb="repair paths --apply")
```

New text:

```
        Path(ctx.args.root)
```

### `r1709.M23_intake_exact_by_token`

intake's exact flag compares the token, so a search for a drop answered by a fire is listed and downloaded

- File: `src/cratekit/intake/candidates.py`
- Source: `r1709.json`, row `M23_intake_exact_by_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3824 against a baseline of 3824
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[the-same-emoji]`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`

Old text:

```
    return frozenset((one.distinct, one.version_key) for one in wanted.readings)

```

New text:

```
    return frozenset((one.recording, one.version_key) for one in wanted.readings)

```

### `r879-a.C10_offset_counts_pages_not_rows`

search_pages: ask offset 1, 2 for the next pages instead of 50, 100

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C10_offset_counts_pages_not_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`

Old text:

```
        pages.append(tuple(search(len(pages) * TRACK_SEARCH_PAGE)))
```

New text:

```
        pages.append(tuple(search(len(pages))))
```

### `r879-a.C11_sole_exact_ignores_full`

sole_exact (existing, sampled): drop the full page condition, so a bound reached answer lists its one exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C11_sole_exact_ignores_full`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_intake_missing_search.py`
- Collected: 106 against a baseline of 106
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
```

New text:

```
    if answer.ambiguous:
```

### `r879-a.C1_full_reads_total_not_last_page`

Answer.full: read the total hits rather than the last page, so a walk that read a full page then a short one still reads as cut short

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C1_full_reads_total_not_last_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_intake_missing_search.py`
- Collected: 106 against a baseline of 106
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
        last = self.hits if self.last_page is None else self.last_page
```

New text:

```
        last = self.hits
```

### `r879-a.C2_walk_ignores_short_page`

search_pages: drop the stop on a short page, so the walk asks every page to the bound

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C2_walk_ignores_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_held_file_whose_isrc_the_account_cannot_name_is_searched_and_said`
  - `tests/test_export_set.py::test_a_held_file_with_no_isrc_is_searched_and_says_so`
  - `tests/test_export_set.py::test_a_short_first_page_is_read_once`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`

Old text:

```
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
```

New text:

```
        if _settled_early(answer) or len(pages) >= bound:
```

### `r879-a.C3_settled_early_without_ambiguity`

_settled_early: drop the ambiguous title, so a title read two ways reads on past a full page

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C3_settled_early_without_ambiguity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound`
  - `tests/test_export_set.py::test_a_title_that_reads_two_ways_reads_no_second_page`

Old text:

```
        answer.ambiguous
        or bool(answer.unreadable)
```

New text:

```
        bool(answer.unreadable)
```

### `r879-a.C4_settled_early_without_unreadable`

_settled_early: drop the unreadable row, so a page with one reads on

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C4_settled_early_without_unreadable`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_unreadable_row_on_a_full_page_reads_no_second_page`

Old text:

```
        or bool(answer.unreadable)

```

New text:

```
        or False

```

### `r879-a.C6_settled_early_without_several`

_settled_early: drop two distinct exact candidates, so a settled several reads a second page

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C6_settled_early_without_several`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_two_exact_matches_on_the_first_page_read_no_second`

Old text:

```
        or len(answer.exact_refs) > 1

```

New text:

```
        or len(answer.exact_refs) > 2

```

### `r879-a.C7_bound_off_by_one`

search_pages: let the bound allow one page more, so the walk asks offset 300, past the ceiling

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C7_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_page_bound_reached_leaves_it_out_and_says_so`
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`

Old text:

```
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
```

New text:

```
        if not answer.full or _settled_early(answer) or len(pages) > bound:
```

### `r879-a.C9_read_pages_forgets_last_page`

read_pages: carry no last page, so a two page answer is judged on its total

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-a.json`, row `C9_read_pages_forgets_last_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_an_empty_page_after_full_ones_ends_the_listing_and_a_full_last_page_never_lists`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_no_exact_match_on_any_page_leaves_it_out_as_none`
  - `tests/test_export_set.py::test_the_same_exact_track_served_again_on_the_next_page_is_one`

Old text:

```
    return replace(answer, pages=len(pages), last_page=len(pages[-1]) if pages else 0)
```

New text:

```
    return replace(answer, pages=len(pages), last_page=None)
```

### `r879-b.C5r_settled_early_without_unnamed_exact`

rerun of C5 after its zero: _settled_early drops the exact candidate with no identifier

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-b.json`, row `C5r_settled_early_without_unnamed_exact`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_exact_match_with_no_identifier_on_a_full_page_reads_no_second_page`

Old text:

```
        or any(not one.track.ref for one in exact)

```

New text:

```
        or False

```

### `r879-b.C8r_ceiling_coefficient`

rerun of C8 after its zero: SEARCH_CEILING 300 to 350, so the derived bound is seven pages

- File: `src/cratekit/intake/candidates.py`
- Source: `r879-b.json`, row `C8r_ceiling_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_walk_never_asks_past_the_providers_ceiling_of_300`

Old text:

```
SEARCH_CEILING = 300
```

New text:

```
SEARCH_CEILING = 350
```

### `u79-a.A1_ambiguous_listed`

A title that reads two ways is listed on one candidate without a person

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A1_ambiguous_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-title-reading]`
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-version-reading]`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.full:
        return None
```

### `u79-a.A2_full_page_listed`

A full page is read as the whole answer, so its one exact hit is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A2_full_page_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.ambiguous:
        return None
```

### `u79-a.A3_unreadable_ignored`

A row of the answer that could not be read no longer stops a listing

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A3_unreadable_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_a_row_that_cannot_be_read_is_offered`

Old text:

```
    if answer.unreadable or not exact:
```

New text:

```
    if not exact:
```

### `u79-a.A4_no_identifier_listed`

Exact candidates carrying no identifier are one distinct value and are listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A4_no_identifier_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`
  - `tests/test_intake_missing_search.py::test_the_only_exact_candidate_carrying_no_identifier_is_not_listed`

Old text:

```
    if any(not one.track.ref for one in exact):
        return None
```

New text:

```
    if False:
        return None
```

### `u79-a.A5_two_exact_picked`

Two exact candidates list the first, the pick the brief forbids

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A5_two_exact_picked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`
  - `tests/test_intake_missing_search.py::test_more_candidates_than_the_screen_holds_are_truncated_and_counted`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if len({one.track.ref for one in exact}) != 1:
```

New text:

```
    if len({one.track.ref for one in exact}) < 1:
```

### `u79-b.B1_floor_halved`

The floor's value is halved, so a weaker hit is shown

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B1_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`

Old text:

```
CANDIDATE_FLOOR = 60.0
```

New text:

```
CANDIDATE_FLOOR = 30.0
```

### `u79-b.B2_score_before_exact`

A near miss scoring 100 leads an exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B2_score_before_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`

Old text:

```
            (not one.exact, -one.score, position, one)
```

New text:

```
            (False, -one.score, position, one)
```

### `u79-b.B3_no_identifier_offered`

A candidate with no identifier is offered as an option

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B3_no_identifier_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_an_exact_one_with_no_identifier_is_offered`
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`

Old text:

```
            if one.track.ref and (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

New text:

```
            if (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

### `u79-b.B4_rejected_read_as_accepted`

A rejected row falls through to the accepted path and its one candidate is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B4_rejected_read_as_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_rejected_row_is_reported_and_never_searched_again`

Old text:

```
    if held.verdict is review.Verdict.REJECTED:
```

New text:

```
    if False:
```

### `u79-b.B5_unspecific_yes_takes_first`

An acceptance naming none of several candidates lists the first

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B5_unspecific_yes_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if chosen is None and len(held.options) == 1:
```

New text:

```
    if chosen is None and len(held.options) >= 1:
```

### `u79-b.B6_option_track_mismatch`

An accepted option whose detail names another track is listed as that track

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B6_option_track_mismatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_option_that_does_not_carry_its_own_track_lists_nothing`

Old text:

```
    if track is None or not track.ref or track.ref != option.option_id:
```

New text:

```
    if track is None or not track.ref:
```

### `u79-b.B8_open_item_searched_again`

A row already in front of a person is searched for again

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B8_open_item_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_near_miss_is_offered_with_its_score_and_is_not_listed`

Old text:

```
    if held.verdict is None:
        return Proposal(
```

New text:

```
    if held.verdict is None:
        return None
    if held.verdict is None:
        return Proposal(
```

### `r1255.F1_refill_plan_unlisted`

plan_refill: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/refill.py`
- Source: `r1255.json`, row `F1_refill_plan_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_refill.py`
- Collected: 28 against a baseline of 28
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
- Ran: `tests/test_inbox_refill.py`, `tests/test_inbox_analyzed.py`
- Collected: 27 against a baseline of 27
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

### `r501-c.M1_export_name_check`

imported_cli.read_export: drop the refusal of an export carrying an intake file's name, leaving only the identity check

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M1_export_name_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
    if any(export.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise _refuse_export(
```

New text:

```
    if False:
        raise _refuse_export(
```

### `r501-c.M2_export_identity_check`

imported_cli.read_export: drop the refusal of the file a waiting run names, so a link to the intake file proves its own import

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M2_export_identity_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
        if artifact and _same_file(export, Path(artifact)):
```

New text:

```
        if False:
```

### `r501-c.M3_missing_is_not_imported`

imported_cli.settle: ignore missing tracks, so an export taken before the import proves it

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M3_missing_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`

Old text:

```
    if missing:
        return {
```

New text:

```
    if False:
        return {
```

### `r501-c.M4_nothing_recorded`

imported_cli.settle: drop the unverifiable answer, so a run the ledger names no file for is proven by any export

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M4_nothing_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`

Old text:

```
    if not landed:
        # NOTHING RECORDED IS NOT NOTHING OWED.
```

New text:

```
    if False:
        # NOTHING RECORDED IS NOT NOTHING OWED.
```

### `r501-c.M5_retire_name_guard`

imported_cli.retire: rename any file a record names, whatever it is called

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M5_retire_name_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_retiring_renames_only_a_plain_file_this_product_named`

Old text:

```
    if not any(artifact.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise refuse(
            "internal-error",
```

New text:

```
    if False:
        raise refuse(
            "internal-error",
```

### `r501-c.M6_retire_link_guard`

imported_cli.retire: follow a link instead of refusing it

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M6_retire_link_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_retiring_renames_only_a_plain_file_this_product_named`

Old text:

```
    if artifact.is_symlink() or not artifact.is_file():
        return None
    if not any(
```

New text:

```
    if not artifact.is_file():
        return None
    if not any(
```

### `r501-d.M10_waiting_legacy`

imported_cli._waiting: look only for awaiting-import, so every landing made before the fix is left where it was

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M10_waiting_legacy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`

Old text:

```
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return (
```

New text:

```
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return False and (
```

### `r501-d.M11_close_refusal_reported`

imported_cli._close_if_nothing_is_owed: raise the gated close's refusal, ending the verb after the file is retired and the proof recorded

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M11_close_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`

Old text:

```
    except CratekitError as exc:
        return {"closed": False, "close_refused": exc.cause.reason, "why": exc.cause.message}
```

New text:

```
    except CratekitError:
        raise
```

### `r501-d.M13_waiting_needs_export`

imported_cli.intake_imported: drop the refusal when a run is waiting and no export is named, so the verb answers no-op over a waiting run

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M13_waiting_needs_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
    if waiting and export is None:
        raise _no_export(waiting)
```

New text:

```
    if waiting and export is None:
        waiting = []
```

### `r501-d.M7_retire_next_free_name`

imported_cli.retire: never take the next free name, so a second retirement lands on the first

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M7_retire_next_free_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_retiring_never_lands_on_another_file`

Old text:

```
        while not naming.claim_target(target):
```

New text:

```
        while False:
```

### `r501-d.M9_waiting_capture`

imported_cli._waiting: drop the no capture condition, so an open destructive session is taken for a landing

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M9_waiting_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1058 against a baseline of 1058
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`

Old text:

```
        record.state is session.SessionState.OPEN
        and record.snapshot_path is None
        and record.pending is None
```

New text:

```
        record.state is session.SessionState.OPEN
        and record.pending is None
```

### `r773-b.P1_proof_granted_whatever_the_export_names`

settle, existing: find no landed track missing, so any export proves any import

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r773-b.json`, row `P1_proof_granted_whatever_the_export_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_imported.py`
- Collected: 131 against a baseline of 131
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_against_an_export_taken_before_the_import`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`

Old text:

```
    missing = [entry for entry in landed if entry.track not in held]
```

New text:

```
    missing = []
```

### `r1499.B01_pass_suffix`

pass_of: any download list's name is a sync pass

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B01_pass_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_only_a_download_over_a_synced_list_is_a_passes`

Old text:

```
    if name == listed or not name.endswith(SYNCED_SUFFIX):
```

New text:

```
    if name == listed:
```

### `r1499.B02_pass_handler`

pass_of: any handler's job over a list is a pass's download

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B02_pass_handler`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name`
  - `tests/test_sync_land_beside.py::test_only_a_download_over_a_synced_list_is_a_passes`

Old text:

```
    if job.handler_key != DOWNLOAD_KEY:
        return None
```

New text:

```
    if False:
        return None
```

### `r1499.B03_pass_step`

Waiting.step: a sync pass's download is named as a plain one, with no continue command

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B03_pass_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_fresh_go_beside_a_sync_passes_download_names_its_continue_command`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        if self.pass_name is not None and self.pass_run is not None:
```

New text:

```
        if False:
```

### `r1499.B04_pass_maybe_renamed`

beside: a sync pass whose tail may have renamed files no download names is never named

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B04_pass_maybe_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`

Old text:

```
            name = pass_of(job) if run is None else None
```

New text:

```
            name = None
```

### `r1499.B05_arrived_items`

arrived: a new finished item of another download is not read

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B05_arrived_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_gos_tail_that_fails_while_a_download_arrives_says_its_record_was_not_kept`

Old text:

```
    new = sorted({job_id for job_id, _item in after.items - before.items})
```

New text:

```
    new = []
```

### `r1499.B06_arrived_count`

arrived: a change in the count of files a landing takes is not read

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B06_arrived_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
    if not new and after.count == before.count:
        return None
```

New text:

```
    if not new:
        return None
```

### `r1499.B08_kept_identity`

beside (sample of the lifted guards): files no download names are all read as own when a record exists

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B08_kept_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_ran_still_refuses_a_file_more_than_its_own_renamed`
  - `tests/test_label_sync_go.py::test_a_go_whose_tracks_left_reads_no_file_put_there_since_as_its_own`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`

Old text:

```
        unnamed = [path for path in unnamed if identity(path) not in kept]
```

New text:

```
        unnamed = []
```

### `r1499.B09_unlistable`

beside (sample of the lifted guards): an unlistable folder reads as empty

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B09_unlistable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_staging_folder_that_cannot_be_listed_refuses_rather_than_hold_nothing`

Old text:

```
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed ({exc}), so whether it "
```

New text:

```
    except OSError:
        held = set()
    if False:
        raise refuse(
            "intake-list-unusable",
            f"the staging folder {folder} could not be listed, so whether it "
```

### `r1499.B10_plain_step_moves_out`

Waiting.step: a plain download's step says to land it in place, which lands the batch with it

- File: `src/cratekit/intake/beside.py`
- Source: `r1499.json`, row `B10_plain_step_moves_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_plain_download_in_the_folder_refuses_a_fresh_go_before_the_gate`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`

Old text:

```
f"move the tracks of job {self.job_id} out of {folder}, and land them on "
```

New text:

```
f"land the tracks of job {self.job_id} in {folder}, and land them on "
```

### `r1255.R3_rotation_warning_gate`

records_warnings: never warn, so the rotation ages a batch from its playlist's date unsaid

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R3_rotation_warning_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read[given0-the session log could not be listed]`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read[given1-2 session record(s) could not be read]`

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
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list_or_records_it_could_not_read[given0-the session log could not be listed]`

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
- Ran: `tests/test_inbox_rotate.py`, `tests/test_cli_contract.py`
- Collected: 1027 against a baseline of 1027
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
- Ran: `tests/test_inbox_rotate.py`, `tests/test_cli_contract.py`
- Collected: 1027 against a baseline of 1027
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

### `u267.M11_rotation_opens_its_own`

rotate_cli.planned: ignore the shared read and open its own handle, a second open in the report

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `u267.json`, row `M11_rotation_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_inbox_rotate.py`
- Collected: 45 against a baseline of 45
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

New text:

```
    one_read = None
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
```

### `r301.R1_seam_falls_back_to_defaults`

The seam builds a default section when none is handed over instead of refusing

- File: `src/cratekit/intake/recognize.py`
- Source: `r301.json`, row `R1_seam_falls_back_to_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_workers.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-section]`

Old text:

```
            raise TypeError(
                "the bound identifier needs the configuration's recognition "
                "section, which names the host and the month's bound"
            )
```

New text:

```
            recognition = config.RecognitionConfig()
```

### `r924.R1_bound_identifier_not_told`

recognize does not hand progress to the bound identifier

- File: `src/cratekit/intake/recognize.py`
- Source: `r924.json`, row `R1_bound_identifier_not_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 78 against a baseline of 78
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
            recognition, refresh=refresh, progress=progress
```

New text:

```
            recognition, refresh=refresh
```

### `u37-author-light.G2_recognition_gate`

Skip the recognition presence gate

- File: `src/cratekit/intake/recognize.py`
- Source: `u37-author-light.json`, row `G2_recognition_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_identification_only_downloads_nothing_and_writes_a_tracklist`

Old text:

```
    missing = recognition_ready()
    if not missing:
        return
    raise refuse(
```

New text:

```
    missing = recognition_ready()
    if True:
        return
    raise refuse(
```

### `u121-b.S25r_bridge_backfill`

_native_or_refuse: a bridge tree is not refused

- File: `src/cratekit/intake/inspiration_cli.py`
- Source: `u121-b.json`, row `S25r_bridge_backfill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_on_the_bridge_is_refused_naming_the_cutover`

Old text:

```
    set_playlist.assert_native(medium, landing=False)
```

New text:

```
    pass
```

### `u121.S24_ack_before_gate`

intake_inspiration: the backup acknowledgment is not read before the gate

- File: `src/cratekit/intake/inspiration_cli.py`
- Source: `u121.json`, row `S24_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `r770-b.B2_gate_asked_before_the_acknowledgment`

ask_then_write: ask the gate without reading the backup acknowledgment first, on both verbs

- File: `src/cratekit/intake/land_native.py`
- Source: `r770-b.json`, row `B2_gate_asked_before_the_acknowledgment`
- Moved: the same acknowledgment read before the gate is asked, in the shared ask then write of the native landing, which U307 moved from land_cli.py to land_native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
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

### `u319.M8_ok_on_any_field`

land_cli: the short path's OK offered whatever the dialog shows

- File: `src/cratekit/intake/land_native.py`
- Source: `u319.json`, row `M8_ok_on_any_field`
- Moved: the same line of the short path's visit wording, which U307 moved from land_cli.py to land_native.py with the native landing
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_intake_land_dyn_native.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 89 against a baseline of 89
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
- Collected: 595 against a baseline of 595
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

