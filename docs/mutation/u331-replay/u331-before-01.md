# Mutation table: u331-before-01

Measured by `scripts/mutate.py` on 2026-11-23 21:16 UTC, branch `HEAD` at `04a5f695`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 228.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 21:16 UTC for commit `04a5f695bb07`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 62, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u327.A10_file_missing_named` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A11_leave_holds` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A12_agreeing_title_left_whole` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 5 | killed |
| `u327.A14_plan_taken_again` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A15_digest_covers_items` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A16_before_values_recorded` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 2 | killed |
| `u327.A17_policy_before_files` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A18_file_read_back` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A19_row_follows_file` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 2 | killed |
| `u327.A1_key_equal_by_wheel` | `src/cratekit/analysis/head_adopt.py` | user | 2 file(s) | 124 | 1 | killed |
| `u327.A20_judge_title` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A22_read_back_refuses_wrong` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A6_key_id_empty` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 3 | killed |
| `u327.A7_not_analysed_left` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A8_no_reference_left` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.A9_tag_body_compared` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u327.B1_unread_intake_refuses` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 77 | 1 | killed |
| `u241.M11_cost_from_the_cheapest_track` | `src/cratekit/analysis/light.py` | user | 1 file(s) | 272 | 13 | killed |
| `u241.M22_decode_not_costed` | `src/cratekit/analysis/light.py` | user | 1 file(s) | 272 | 29 | killed |
| `u275.M1_base_back_to_linux` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 6 | killed |
| `u275.M2_slope_back_to_linux` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 19 | killed |
| `u275.M3_slope_rounded_down` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 6 | killed |
| `u275.M4_base_rounded_down` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 5 | killed |
| `u275.M5_decode_line_dropped` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 29 | killed |
| `u275.M6_unknown_length_shorter` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 3 | killed |
| `u275.M7_cheapest_track_sets_the_cost` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 13 | killed |
| `u275.M8_analysis_line_scaled` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 550 | 18 | killed |
| `a32.R1_gate_not_explicit` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1079 | 5 | killed |
| `r185-r246-author.D2_cloud_gate_restored` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5811 | 2 | killed |
| `r312.R1_summary_promises_a_replace` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5811 | 1 | killed |
| `r372-b.B12_verb_does_not_declare_the_check` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1487 | 1 | killed |
| `r424.A1_writes_narrowed` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1142 | 2 | killed |
| `r424.A2_cloud_gate_absent` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1142 | 2 | killed |
| `r424.A3_rekordbox_checks` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1559 | 1 | killed |
| `r424.A4_library_mounted` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1559 | 1 | killed |
| `r424.A5_summary_both_ways` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1142 | 1 | killed |
| `r770-d.C8_native_gate_answered_inline` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1052 | 6 | killed |
| `r773-b.R1_doctor_check_not_declared` | `src/cratekit/cli/registry.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `r923.N20_gate_takes_inline_answer` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 53 | 5 | killed |
| `u103-b.M1_identify_declared_adjudicating` | `src/cratekit/cli/registry.py` | maintainer | 2 file(s) | 1085 | collection error | collect-error |
| `u129-author.A10_export_set_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 20 | 1 | killed |
| `u129-author.A11_export_archive_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 20 | 1 | killed |
| `u129-author.A9_land_without_provider_check` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 20 | 1 | killed |
| `u263.D22_restamp_declares` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1436 | 1 | killed |
| `u27-adopt-apply-author.R1_marker_restored` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1732 | collection error | collect-error |
| `u27-reports-round-1.R1_delete_review_precondition` | `src/cratekit/cli/registry.py` | user | 14 file(s) | 3877 | 2 | killed |
| `u27-restore-cli-independent.I_H1_the_landed_verb_keeps_its_marker` | `src/cratekit/cli/registry.py` | maintainer | 2 file(s) | 1117 | collection error | collect-error |
| `u28-skills-independent.R1_planned_in_restored` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 1015 | collection error | collect-error |
| `u39-author-full.W2_unreachable_gate_restored` | `src/cratekit/cli/registry.py` | user | 19 file(s) | 4040 | 1 | killed |
| `u40-author-full.R3_ungated` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 1019 | 1 | killed |
| `u40-author-full.R5_row_unclaimed` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1027 | 5 | killed |
| `u40-author-full.R6_row_still_cut` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1027 | 1 | killed |
| `u42-author-round-2.R2_handler_lookup_imports` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 1019 | 1 | killed |
| `u42-author.R1_planned_marker_returns` | `src/cratekit/cli/registry.py` | user | 3 file(s) | 1048 | collection error | collect-error |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry.py` | maintainer | 21 file(s) | 4166 | collection error | collect-error |
| `u44-author.D1_registry_drops_long_running` | `src/cratekit/cli/registry.py` | maintainer | 22 file(s) | 4226 | collection error | collect-error |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4336 | collection error | collect-error |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4339 | collection error | collect-error |
| `u69-b.M20_registry_schema` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1059 | 24 | killed |
| `u72.M8_registry_digest_source` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 27 | 7 | killed |
| `u91.G1_registry_xml` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1216 | 1 | killed |
| `u96-b.B1_no_library_check_declared` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1113 | 1 | killed |
| `r722-b.T6_field_failure_swallowed` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2982 | 1 | killed |
| `r722-b.T7_lenient_field_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2982 | 1 | killed |
| `r722.T1_checked_is_lenient` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2982 | 5 | killed |
| `r722.T3_open_failure_is_absent` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2982 | 3 | killed |
| `r722.T8_lenient_energy_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2982 | 1 | killed |
| `r722.T9_lenient_open_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2982 | 305 | killed |
| `u23-round-8-independent-hunt.HUNT_a_container_leaves_the_writers_table` | `src/cratekit/core/tags.py` | user | 2 file(s) | 628 | collection error | collect-error |
| `u23-round-8-independent.X15_save_drops_the_id3v1_trailer` | `src/cratekit/core/tags.py` | user | 3 file(s) | 854 | 1 | killed |
| `u240.M25_copyright_key_wrong` | `src/cratekit/core/tags.py` | user | 5 file(s) | 337 | 1 | killed |
| `u249.M15_noting_reader_drops_field_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 692 | 1 | killed |
| `u249.M16_noting_reader_drops_open_failure` | `src/cratekit/core/tags.py` | user | 3 file(s) | 692 | 2 | killed |
| `u249.M17_noting_reader_drops_unrecognised` | `src/cratekit/core/tags.py` | user | 3 file(s) | 692 | 3 | killed |
| `u249.M18_noting_reader_drops_unsupported` | `src/cratekit/core/tags.py` | maintainer | 3 file(s) | 692 | 1 | killed |
| `u249.M19_noting_reader_inverted` | `src/cratekit/core/tags.py` | user | 3 file(s) | 692 | 6 | killed |
| `u250.M5_word_reads_zero` | `src/cratekit/core/tags.py` | user | 3 file(s) | 212 | 1 | killed |
| `u250.M6_absent_raises` | `src/cratekit/core/tags.py` | user | 3 file(s) | 212 | 20 | killed |
| `u250.M7_energy_word_reads_absent` | `src/cratekit/core/tags.py` | user | 4 file(s) | 125 | 2 | killed |
| `u250.M8_conversion_learns_decimals` | `src/cratekit/core/tags.py` | user | 3 file(s) | 212 | 1 | killed |
| `u301.T1_refuse_unknown_admits_a_field` | `src/cratekit/core/tags.py` | user | 3 file(s) | 168 | 1 | killed |
| `u301.T3_rewrite_reports_a_failed_save` | `src/cratekit/core/tags.py` | user | 3 file(s) | 223 | 1 | killed |
| `u301.T4_spec_admits_an_unknown_field` | `src/cratekit/core/tags.py` | user | 3 file(s) | 150 | 2 | killed |
| `u81-fetch-b.S1_strip_does_nothing` | `src/cratekit/core/tags.py` | user | 1 file(s) | 35 | 2 | killed |
| `r1467.M19_root_unreadable_refuses` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M20_retired_file_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M21_native_record_proves` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
| `r1467.M22_proof_is_a_file` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 276 | 1 | killed |
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
| `u120.C2_hearts_not_claimed` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 13 | 10 | killed |
| `u121-b.S20r_bridge_set` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u127.L6_bridge_ignores_calibration` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 454 | 1 | killed |
| `u128-b.B3_owned_unresolved_at_gate` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 4 | killed |
| `u128.L1_bridge_warning_unsaid` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `u129-author.A19_plan_archive_always_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 3 | killed |
| `u146-c.L2_empty_landing_no_op` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 12 | 4 | killed |
| `u156.L23_label_beside_manifest` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 90 | 1 | killed |
| `u156.L24_label_on_the_bridge` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 117 | 2 | killed |
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
| `u165.L3_filing_tail` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 98 | 3 | killed |
| `u177.C3_flag_beside_label` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u188.M10_detail_mapped_dropped` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 25 | 1 | killed |
| `u188.M11_fields_last_part` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M12_fields_keep_indices` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M13_fields_repeated` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M1_stored_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M2_scratch_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M3_live_stored_under_the_mount` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M4_staging_pair_dropped` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 18 | killed |
| `u188.M5_repeat_kept` | `src/cratekit/intake/land_cli.py` | maintainer | 1 file(s) | 22808 | 0 (promoted) | zero |
| `u188.M6_mapped_as_lines` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M7_signs_swapped` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 2 | killed |
| `u188.M8_fields_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M9_pairs_left_out` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u307.R20_land_only_by_default` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 36 | 5 | killed |
| `u307.R21_unrunnable_reason_lost` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 3 | killed |
| `u307.R4_land_cli_getattr_answers_none` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 116 | 23 | killed |
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
| `u72.M7_gate_digest_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 22808 | 5 (promoted) | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u77-c.C6_gate_manifest_bytes` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-c.C7_digest_handed_to_engine` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 1 | killed |
| `u77-c.C8_unfiled_rows_warned` | `src/cratekit/intake/land_cli.py` | user | 6 file(s) | 254 | 2 | killed |

## Zero rows and what they owe

- `u188.M5_repeat_kept` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u327.A10_file_missing_named`

_resolved: answer a missing file as present, so it is named unreadable rather than missing

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A10_file_missing_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_gone_before_the_plan_is_left_and_named`

Old text:

```
    return (path, "") if present else (path, FILE_MISSING)
```

New text:

```
    return (path, "")
```

### `u327.A11_leave_holds`

plan_adopt: ignore --leave, so a row held out is written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A11_leave_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_leave_holds_a_row_out_in_the_plan_and_on_the_apply`

Old text:

```
        if item.action == ADOPT and content_id in held:
```

New text:

```
        if False:
```

### `u327.A12_agreeing_title_left_whole`

plan_row: drop the agreeing title return, so a blank key tag beside an agreeing head is filled

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A12_agreeing_title_left_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 5 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_missing_key_never_stops_the_tempo_nor_a_missing_tempo_the_key`
  - `tests/test_analyze_adopt.py::test_a_second_run_plans_nothing_still_asks_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_the_old_values_are_on_disk_before_the_first_file_is_written`
  - `tests/test_analyze_adopt.py::test_the_plan_shows_each_row_before_and_after_with_its_key_relation_and_tempo`
  - `tests/test_analyze_adopt.py::test_the_record_keeps_every_surface_s_old_value_for_a_restore`

Old text:

```
    if new_title == title and new_tag == tag_title:
```

New text:

```
    if False:
```

### `u327.A14_plan_taken_again`

assert_plan_unchanged: never refuse, so a plan that moved after the gate is written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A14_plan_taken_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_plan_that_moves_on_the_write_handle_refuses_before_any_file`

Old text:

```
    if again.digest == approved.digest:
        return
```

New text:

```
    if True:
        return
```

### `u327.A15_digest_covers_items`

AdoptPlan.digest: digest the counts and not the items, so a changed answer with the same counts is approved

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A15_digest_covers_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_title_changed_between_plan_and_apply_refuses_and_writes_nothing`

Old text:

```
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
```

New text:

```
                "counts": dict(self.counts),
```

### `u327.A16_before_values_recorded`

apply_adopt: keep no surface's old value in the session record

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A16_before_values_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_old_values_are_on_disk_before_the_first_file_is_written`
  - `tests/test_analyze_adopt.py::test_the_record_keeps_every_surface_s_old_value_for_a_restore`

Old text:

```
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes]

```

New text:

```
(empty)
```

### `u327.A17_policy_before_files`

apply_adopt: drop the policy check before the first file, so a plan naming another column writes the files and the title

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A17_policy_before_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_plan_that_would_write_the_tempo_column_is_refused_by_policy`

Old text:

```
    metadata.assert_within_policy(row_changes(writes))

```

New text:

```
(empty)
```

### `u327.A18_file_read_back`

write_files: trust the write, so a file that does not read back as planned has its row written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A18_file_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_that_does_not_read_back_keeps_its_row_s_title_and_is_named`

Old text:

```
        if unreadable or title != item.new_tag_title or initialkey != item.new_initialkey:
```

New text:

```
        if unreadable:
```

### `u327.A19_row_follows_file`

apply_adopt: write a row whose file did not take, so the title and the tag disagree

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A19_row_follows_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_that_cannot_be_written_keeps_its_row_s_title_and_is_named`
  - `tests/test_analyze_adopt.py::test_a_file_that_does_not_read_back_keeps_its_row_s_title_and_is_named`

Old text:

```
        rowed = [item for item in writes if item.content_id in landed and item.writes_title]
```

New text:

```
        rowed = [item for item in writes if item.writes_title]
```

### `u327.A1_key_equal_by_wheel`

adopted: compare the written key to rekordbox's as text, so an unpadded spelling of the same key is rewritten

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A1_key_equal_by_wheel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_head_takes_rekordbox_s_key_and_tempo_and_no_other_byte[unpadded-equal-stands]`

Old text:

```
    if key is not None and parse_camelot(written_key) != parse_camelot(key):
```

New text:

```
    if key is not None and written_key != key:
```

### `u327.A20_judge_title`

judge: never read the title back, so a row that does not carry its new title passes

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A20_judge_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_read_back_names_a_title_not_carried_and_a_column_moved`

Old text:

```
        if str(now.get("Title") or "") != item.new_title:
```

New text:

```
        if False:
```

### `u327.A22_read_back_refuses_wrong`

assert_read_back: refuse only a moved column, so a title that does not read back ends ok

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A22_read_back_refuses_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_read_back_wrong_or_moved_refuses_naming_the_session_that_undoes_it`

Old text:

```
    elif written.wrong:
```

New text:

```
    elif False:
```

### `u327.A6_key_id_empty`

reference_key: drop the empty KeyID check, so a KeyID of zero beside a named key row is read as a key

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A6_key_id_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_key_column_reads_in_either_notation_or_says_why_it_does_not[0-8A-expected10]`
  - `tests/test_analyze_adopt.py::test_the_key_column_reads_in_either_notation_or_says_why_it_does_not[0-8A-expected9]`
  - `tests/test_analyze_adopt.py::test_the_key_column_reads_in_either_notation_or_says_why_it_does_not[None-8A-expected8]`

Old text:

```
    if key_id in rb_writer.FIELD_EMPTIES["KeyID"] or not str(scale_name or "").strip():
```

New text:

```
    if not str(scale_name or "").strip():
```

### `u327.A7_not_analysed_left`

plan_row: drop the not analysed guard, so a row rekordbox has not analysed is planned off its unread columns

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A7_not_analysed_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`

Old text:

```
    if judged.action != analyzed.CLEAR:
```

New text:

```
    if False:
```

### `u327.A8_no_reference_left`

plan_row: drop the no answer guard, so a row with neither key nor tempo reads as agreeing

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A8_no_reference_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_missing_key_never_stops_the_tempo_nor_a_missing_tempo_the_key`

Old text:

```
    if key is None and tempo is None:
```

New text:

```
    if False:
```

### `u327.A9_tag_body_compared`

plan_row: drop the title tag body comparison, so a file whose tag names another title is rewritten

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A9_tag_body_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`

Old text:

```
    if new_tag is None or split_head(tag_title, template=template)[1] != split_head(
        title, template=template
    )[1]:
```

New text:

```
    if new_tag is None:
```

### `u327.B1_unread_intake_refuses`

head_adopt.resolve_scope: drop the read of the intake root, so an INBOX / Analyze nobody could read plans as empty

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `B1_unread_intake_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_an_intake_tree_that_cannot_be_read_refuses_before_the_gate`

Old text:

```
    refill.anchored_root(db, declared.intake.id, registry)
    members, why = rc._analyze_members(db, declared, registry)
```

New text:

```
    members, why = rc._analyze_members(db, declared, registry)
```

### `u241.M11_cost_from_the_cheapest_track`

light.costliest: the cheapest track sets the worker's cost

- File: `src/cratekit/analysis/light.py`
- Source: `u241.json`, row `M11_cost_from_the_cheapest_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[64]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[6]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[8]`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[12]`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[8]`

Old text:

```
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)

```

New text:

```
    return min((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)

```

### `u241.M22_decode_not_costed`

light.worker_bytes: the decode's line is dropped, so a 192 kilohertz file is declared at its length alone, 1310 MB where 2180 was measured

- File: `src/cratekit/analysis/light.py`
- Source: `u241.json`, row `M22_decode_not_costed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 29 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-86400.0]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    return LIGHT_BASE_BYTES + max(analysis, decode)

```

New text:

```
    return LIGHT_BASE_BYTES + analysis

```

### `u275.M1_base_back_to_linux`

LIGHT_BASE_BYTES back to U241's 320 megabytes, the figure before the Mac was measured

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M1_base_back_to_linux`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BASE_BYTES = 384 * 1024 * 1024
```

New text:

```
LIGHT_BASE_BYTES = 320 * 1024 * 1024
```

### `u275.M2_slope_back_to_linux`

LIGHT_BYTES_PER_SECOND back to U241's 1.5 megabytes a second, under every Mac peak

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M2_slope_back_to_linux`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 19 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[376-1281]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[576-1805]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[668-2105]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[690-2162]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
```

New text:

```
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024 // 2
```

### `u275.M3_slope_rounded_down`

LIGHT_BYTES_PER_SECOND rounded down to 3.0 megabytes a second, over every peak but under a ninth above the measured slope

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M3_slope_rounded_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
```

New text:

```
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024
```

### `u275.M4_base_rounded_down`

LIGHT_BASE_BYTES rounded down to 352 megabytes, over the measured intercept but under an eighth above it

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M4_base_rounded_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BASE_BYTES = 384 * 1024 * 1024
```

New text:

```
LIGHT_BASE_BYTES = 352 * 1024 * 1024
```

### `u275.M5_decode_line_dropped`

worker_bytes: drop the decode line, so a 192 kHz file costs only its length's analysis line

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M5_decode_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 29 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-86400.0]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    return LIGHT_BASE_BYTES + max(analysis, decode)
```

New text:

```
    return LIGHT_BASE_BYTES + analysis
```

### `u275.M6_unknown_length_shorter`

_shape_of: bound an unknown length at fifty times the slowest rate, so not knowing plans wider than knowing

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M6_unknown_length_shorter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_whose_length_is_unknown_costs_no_less_than_before`
  - `tests/test_analysis_ahead.py::test_a_file_whose_length_is_unknown_is_still_planned_narrower`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`

Old text:

```
            seconds = target.stat().st_size / SLOWEST_BYTES_PER_SECOND
```

New text:

```
            seconds = target.stat().st_size / (SLOWEST_BYTES_PER_SECOND * 50)
```

### `u275.M7_cheapest_track_sets_the_cost`

costliest: take the cheapest track's cost, so a folder's longest track no longer sets the plan

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M7_cheapest_track_sets_the_cost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[64]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[6]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[8]`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[12]`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[8]`

Old text:

```
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)
```

New text:

```
    return min((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)
```

### `u275.M8_analysis_line_scaled`

worker_bytes: the analysis line at three quarters of the declared slope, a coefficient mutation

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M8_analysis_line_scaled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 550 against a baseline of 550
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[376-1281]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[576-1805]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[668-2105]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[690-2162]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND)
```

New text:

```
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND * 3 // 4)
```

### `a32.R1_gate_not_explicit`

The confirm gate is answerable inline

- File: `src/cratekit/cli/registry.py`
- Source: `a32.json`, row `R1_gate_not_explicit`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; repair.link.confirm's explicit flag is the same value, flipped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_cli_contract.py`
- Collected: 1079 against a baseline of 1079
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`

Old text:

```
                prompt="Write these probe values onto these rows?",
                #: Explicit (R34): a write to a row of a live library.
                explicit=True, digest_source="plan",
```

New text:

```
                prompt="Write these probe values onto these rows?",
                #: Explicit (R34): a write to a row of a live library.
                explicit=False, digest_source="plan",
```

### `r185-r246-author.D2_cloud_gate_restored`

Declare the cloud sync decision on a verb that opens no database, the half the contract suite calls spurious

- File: `src/cratekit/cli/registry.py`
- Source: `r185-r246-author.json`, row `D2_cloud_gate_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the cloud sync gate is added to tag.retag's gates, the entry before name.apply, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5811 against a baseline of 5811
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_tag_workers.py::test_the_retag_entry_declares_the_file_surface_alone_and_no_database_decision`

Old text:

```
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="name.apply",
```

New text:

```
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="name.apply",
```

### `r312.R1_summary_promises_a_replace`

Put the registry summary back to the promise the verb does not keep

- File: `src/cratekit/cli/registry.py`
- Source: `r312.json`, row `R1_summary_promises_a_replace`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; route.resort's summary is the same string, now in parentheses, replaced by the same text
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5811 against a baseline of 5811
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_resort_summary_says_the_verb_is_additive`

Old text:

```
        summary=(
            "add already-routed tracks to their new place after a genre or energy "
            "change, additive, the old membership stays and is named"
        ),
```

New text:

```
        summary="re-place already-routed tracks after a genre or energy change",
```

### `r372-b.B12_verb_does_not_declare_the_check`

registry: the My Tags verb stops declaring library.paths_resolved

- File: `src/cratekit/cli/registry.py`
- Source: `r372-b.json`, row `B12_verb_does_not_declare_the_check`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; metadata.mytags-vocals still declares library.paths_resolved under the comment, and the row drops it the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1487 against a baseline of 1487
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_the_verb_declares_the_check_and_the_slug_is_registered`

Old text:

```
            # The ratio the verb refuses on, unmapped rows tag nothing (R-372).
            "library.paths_resolved",
```

New text:

```
            # The ratio the verb refuses on, unmapped rows tag nothing (R-372).
```

### `r424.A1_writes_narrowed`

Restore the four local write surfaces the verb never reaches

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A1_writes_narrowed`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; sync.favorites' write surface is the same set, widened the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1142 against a baseline of 1142
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_outbound_workers.py::test_the_verb_declares_the_remote_account_and_no_local_surface`

Old text:

```
        writes=frozenset({"remote"}), adjudicates=True, destructive=True,
```

New text:

```
        writes=frozenset({"db_tree", "db_metadata", "xml", "files", "remote"}), adjudicates=True, destructive=True,
```

### `r424.A2_cloud_gate_absent`

Restore the cloud sync decision on a verb that never opens the database

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A2_cloud_gate_absent`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the cloud sync gate is added to sync.favorites' gates, before its landed comment, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1142 against a baseline of 1142
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`
  - `tests/test_outbound_workers.py::test_the_verb_asks_no_question_its_work_cannot_raise`

Old text:

```
                explicit=True, digest_source="plan",
            ),
        ),
        # Landed (U33, R-130).
```

New text:

```
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        # Landed (U33, R-130).
```

### `r424.A3_rekordbox_checks`

Restore both rekordbox doctor checks for a verb that reads an export

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A3_rekordbox_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`, `tests/test_doctor.py`
- Collected: 1559 against a baseline of 1559
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_doctor_asks_neither_rekordbox_question_for_a_sweep_that_reads_an_export`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

### `r424.A4_library_mounted`

Drop library.mounted, which the outbound write ledger needs

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A4_library_mounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`, `tests/test_doctor.py`
- Collected: 1559 against a baseline of 1559
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_doctor_asks_neither_rekordbox_question_for_a_sweep_that_reads_an_export`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.favorites.confirm",
```

### `r424.A5_summary_both_ways`

Restore the summary that claims the verb moves favourites both ways

- File: `src/cratekit/cli/registry.py`
- Source: `r424.json`, row `A5_summary_both_ways`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1142 against a baseline of 1142
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_verb_declares_the_remote_account_and_no_local_surface`

Old text:

```
        summary="heart the library's favourites on the streaming service; add-only, never un-hearts",
```

New text:

```
        summary="sync hearted tracks both ways; add-only, never un-hearts",
```

### `r770-d.C8_native_gate_answered_inline`

registry: declare intake.file.native as an ordinary gate, answerable on the run that found it

- File: `src/cratekit/cli/registry.py`
- Source: `r770-d.json`, row `C8_native_gate_answered_inline`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; intake.file.native's explicit flag is the same value, flipped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_cli_contract.py`
- Collected: 1052 against a baseline of 1052
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
                prompt="Add this file to the collection?", explicit=True, digest_source="plan",
```

New text:

```
                prompt="Add this file to the collection?", explicit=False, digest_source="plan",
```

### `r773-b.R1_doctor_check_not_declared`

registry: the verb no longer declares library.paths_resolved

- File: `src/cratekit/cli/registry.py`
- Source: `r773-b.json`, row `R1_doctor_check_not_declared`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_verb_declares_one_xml_no_database_surface_and_asks_nothing`

Old text:

```
        doctor_checks=("library.mounted", "rekordbox.closed", "library.paths_resolved"),
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.closed"),
```

### `r923.N20_gate_takes_inline_answer`

The repair's gate accepts an inline answer, so a flag on the command writes the rows

- File: `src/cratekit/cli/registry.py`
- Source: `r923.json`, row `N20_gate_takes_inline_answer`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; repair.rows.confirm's explicit flag is the same value, flipped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
                prompt="Give these rows rekordbox's own defaults?",
                #: Explicit (R34): a write to rows of a live library.
                explicit=True, digest_source="plan",
```

New text:

```
                prompt="Give these rows rekordbox's own defaults?",
                #: Explicit (R34): a write to rows of a live library.
                explicit=False, digest_source="plan",
```

### `u103-b.M1_identify_declared_adjudicating`

Take the adjudicates declaration off intake.identify

- File: `src/cratekit/cli/registry.py`
- Source: `u103-b.json`, row `M1_identify_declared_adjudicating`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; intake.identify's adjudicates flag is the same value, dropped the same way
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_cli_contract.py`
- Collected: 1085 against a baseline of 1086
- Kills: 1 (collect-error)
- Note: collection changed: 1085 collected against a baseline of 1086. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/intake/test_workers.py::test_the_intake_keys_resolve_to_the_one_worker_and_the_job_verbs_spell_them_alike`

Old text:

```
        adjudicates=True, emits=frozenset({"match"}), output_schema="match/1",
```

New text:

```
        emits=frozenset({"match"}), output_schema="match/1",
```

### `u129-author.A10_export_set_without_library_mounted`

Drop library.mounted from export.set so the INSPIRATION backfill opens a database doctor never checked

- File: `src/cratekit/cli/registry.py`
- Source: `u129-author.json`, row `A10_export_set_without_library_mounted`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; export.set's checks are the same tuple, library.mounted dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_intake_set_declares_the_account_gate_and_remote_write`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.set.confirm",
```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.set.confirm",
```

### `u129-author.A11_export_archive_without_library_mounted`

Drop library.mounted from export.archive so the no-name backfill opens library paths doctor never checked

- File: `src/cratekit/cli/registry.py`
- Source: `u129-author.json`, row `A11_export_archive_without_library_mounted`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; export.archive's checks are the same tuple, library.mounted dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_intake_set_declares_the_account_gate_and_remote_write`

Old text:

```
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.archive.confirm",
```

New text:

```
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.archive.confirm",
```

### `u129-author.A9_land_without_provider_check`

Drop credential.provider from intake.land so doctor never names the archive's session

- File: `src/cratekit/cli/registry.py`
- Source: `u129-author.json`, row `A9_land_without_provider_check`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; intake.land's checks are the same tuple, credential.provider dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_intake_set_declares_the_account_gate_and_remote_write`

Old text:

```
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
            "credential.provider",
        ),
```

New text:

```
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
```

### `u263.D22_restamp_declares`

registry: analyze restamp no longer declares binary.ffmpeg

- File: `src/cratekit/cli/registry.py`
- Source: `u263.json`, row `D22_restamp_declares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1436 against a baseline of 1436
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_ffmpeg_names_the_analysis_whose_decoder_it_is`

Old text:

```
        doctor_checks=("library.mounted", "rekordbox.pins", "binary.ffmpeg"),
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.pins"),
```

### `u27-adopt-apply-author.R1_marker_restored`

Put planned_in back on the entry, so the conformance suite stops driving the landed verb

- File: `src/cratekit/cli/registry.py`
- Source: `u27-adopt-apply-author.json`, row `R1_marker_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on adopt.move, the entry before the deletion heading, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adoption.py`, `tests/test_pending_units.py`
- Collected: 1732 against a baseline of 1735
- Kills: 3 (collect-error)
- Note: collection changed: 1732 collected against a baseline of 1735. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adoption.py::test_no_landed_adoption_verb_still_owes_the_file_the_board_reads`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cli_contract.py::test_every_verb_acknowledged_for_conformance_is_refused_without_one_elsewhere`

Old text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, two modules
```

New text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        planned_in=ADOPT_APPLY_CLI_UNIT,
    ),
    # ── Deletion: one surface, two modules
```

### `u27-reports-round-1.R1_delete_review_precondition`

Stop delete.review declaring the Trash check as a precondition

- File: `src/cratekit/cli/registry.py`
- Source: `u27-reports-round-1.json`, row `R1_delete_review_precondition`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; delete.review's checks are the same tuple, library.trash dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 3877 against a baseline of 3877
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_trash_probe_the_operating_system_refuses_is_a_failure_with_the_right_act`
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
            "library.mounted", "library.identity", "library.trash", "rekordbox.closed",
```

New text:

```
            "library.mounted", "library.identity", "rekordbox.closed",
```

### `u27-restore-cli-independent.I_H1_the_landed_verb_keeps_its_marker`

Put planned_in back on restore.list, which is what would disarm the conformance properties again

- File: `src/cratekit/cli/registry.py`
- Source: `u27-restore-cli-independent.json`, row `I_H1_the_landed_verb_keeps_its_marker`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on restore.list, above its landed comment, as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_pending_units.py`
- Collected: 1117 against a baseline of 1120
- Kills: 1 (collect-error)
- Note: collection changed: 1117 collected against a baseline of 1120. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        # Landed (U27); three of the nine conformance properties arm against it.
```

New text:

```
        planned_in="U27",
        # Landed (U27); three of the nine conformance properties arm against it.
```

### `u28-skills-independent.R1_planned_in_restored`

the skills.install registry entry gets planned_in back, so the conformance properties skip it again

- File: `src/cratekit/cli/registry.py`
- Source: `u28-skills-independent.json`, row `R1_planned_in_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on skills.install, after its schema, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1015 against a baseline of 1019
- Kills: 1 (collect-error)
- Note: collection changed: 1015 collected against a baseline of 1019. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        output_schema="diagnostic/1",
        # Landed (U28).
```

New text:

```
        output_schema="diagnostic/1",
        planned_in="U28",
        # Landed (U28).
```

### `u39-author-full.W2_unreachable_gate_restored`

name.apply redeclares the cloud sync decision its work can never raise

- File: `src/cratekit/cli/registry.py`
- Source: `u39-author-full.json`, row `W2_unreachable_gate_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the cloud sync gate is added to name.apply's gates, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 4040 against a baseline of 4040
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

Old text:

```
                prompt="Apply these renames?", digest_source="plan",
            ),
        ),
```

New text:

```
                prompt="Apply these renames?", digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
```

### `u40-author-full.R3_ungated`

Drop the module toggle, so a Module row ships on in the slim profile (R5)

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R3_ungated`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; tag.retag's module toggle is the same value, dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1019 against a baseline of 1019
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`

Old text:

```
        module_id="repair", argv_builder="retag_argv", long_running=True,
```

New text:

```
        argv_builder="retag_argv", long_running=True,
```

### `u40-author-full.R5_row_unclaimed`

Claim no feature row, so row 18 becomes a Module the product owes and no verb cites

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R5_row_unclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1027 against a baseline of 1027
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cutover_parity.py::test_a_row_cited_by_nothing_is_a_decision_and_not_an_oversight`
  - `tests/test_cutover_parity.py::test_the_backlog_is_every_owed_row_without_a_landed_verb`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`

Old text:

```
        feature_rows=(18,),
```

New text:

```
        feature_rows=(),
```

### `u40-author-full.R6_row_still_cut`

Leave row 18 dispositioned Cut while a verb claims it, which is the coupling across two trees

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R6_row_still_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1027 against a baseline of 1027
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`

Old text:

```
    Feature(18, "genre correction for a tag already too coarse", "module"),
```

New text:

```
    Feature(18, "genre correction for a tag already too coarse", "cut"),
```

### `u42-author-round-2.R2_handler_lookup_imports`

Make by_handler_key import the module, which is what the rewritten guard forbids

- File: `src/cratekit/cli/registry.py`
- Source: `u42-author-round-2.json`, row `R2_handler_lookup_imports`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1019 against a baseline of 1019
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_handler_key_resolves_without_importing_the_module`

Old text:

```
def by_handler_key(key: str) -> Entry:
```

New text:

```
def by_handler_key(key: str) -> Entry:
    import importlib

    importlib.import_module("cratekit.acquire.cli")
```

### `u42-author.R1_planned_marker_returns`

Restore planned_in on acquire.download, which is the state that hid rows 6 and 7

- File: `src/cratekit/cli/registry.py`
- Source: `u42-author.json`, row `R1_planned_marker_returns`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on acquire.download, above its landed comment, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_cutover_parity.py`, `tests/test_cli_contract.py`
- Collected: 1048 against a baseline of 1051
- Kills: 7 (collect-error)
- Note: collection changed: 1048 collected against a baseline of 1051. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_cli.py::test_download_on_an_absent_job_refuses_with_a_vocabulary_code`
  - `tests/test_acquire_cli.py::test_download_over_an_absent_list_refuses_by_name`
  - `tests/test_acquire_cli.py::test_download_reaches_no_provider_and_no_network`
  - `tests/test_acquire_cli.py::test_the_verb_appears_in_help_and_dispatches[acquire.download]`
  - `tests/test_acquire_cli.py::test_the_verb_is_landed_rather_than_planned[acquire.download]`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        # Landed (U42).
```

New text:

```
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        planned_in="U15",
        # Landed (U42).
```

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on setbuild, above its landed comment, as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4166 against a baseline of 4170
- Kills: 33 (collect-error)
- Note: collection changed: 4166 collected against a baseline of 4170. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[empty-anchor]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-name]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-path]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[path-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[tempo-beside-path]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[unowned-no-key]`
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        emits=frozenset({"plan"}), output_schema="plan/1",
        # Landed (U43).
```

New text:

```
        emits=frozenset({"plan"}), output_schema="plan/1",
        planned_in="U35",
        # Landed (U43).
```

### `u44-author.D1_registry_drops_long_running`

Remove long_running from the master entry, which should shrink two derived populations

- File: `src/cratekit/cli/registry.py`
- Source: `u44-author.json`, row `D1_registry_drops_long_running`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; master's long_running flag is the same value, dropped the same way
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4226 against a baseline of 4227
- Kills: 2 (collect-error)
- Note: collection changed: 4226 collected against a baseline of 4227. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`
  - `tests/test_master_cli.py::test_the_entry_is_landed_declares_no_gate_and_is_absent_from_a_slim_profile`

Old text:

```
argv_builder="master_argv", long_running=True,
```

New text:

```
argv_builder="master_argv",
```

### `u45-round-1.V3_marker_restored`

Put planned_in back, so the verb reads as unlanded and every conformance property stops arming against it

- File: `src/cratekit/cli/registry.py`
- Source: `u45-round-1.json`, row `V3_marker_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on backup.run, above its landed comment, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4336 against a baseline of 4340
- Kills: 49 (collect-error)
- Note: collection changed: 4336 collected against a baseline of 4340. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`
  - `tests/test_backup_cli.py::test_a_backup_to_a_destination_nobody_is_backing_up_to_is_its_own_job`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        # Landed (U45).
```

New text:

```
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        planned_in="U35",
        # Landed (U45).
```

### `u45-round-1.V5_module_toggle_dropped`

Drop the module toggle, so the verb is offered on a slim install that has no backup module

- File: `src/cratekit/cli/registry.py`
- Source: `u45-round-1.json`, row `V5_module_toggle_dropped`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; backup.run's module toggle is the same value, dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4339 against a baseline of 4340
- Kills: 6 (collect-error)
- Note: collection changed: 4339 collected against a baseline of 4340. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_the_verb_is_declared_landed_and_names_this_module`
  - `tests/test_backup_cli.py::test_the_verb_is_offered_on_the_full_profile_and_withheld_on_the_slim_one`
  - `tests/test_cli_contract.py::test_every_declared_module_toggle_is_used_by_at_least_one_verb`
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cli_contract.py::test_every_live_toggle_is_driven_by_the_toggle_test_below`
  - `tests/test_doctor.py::test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure`

Old text:

```
source_scripts=("backup.sh",), module_id="backup",
```

New text:

```
source_scripts=("backup.sh",),
```

### `u69-b.M20_registry_schema`

Declare the verb plan/1 in the registry, which the human renderer does not show

- File: `src/cratekit/cli/registry.py`
- Source: `u69-b.json`, row `M20_registry_schema`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; intake.missing's schema is the same pair, swapped to plan the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 24 (killed)
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
  - ... and 9 more, see the JSON sidecar

Old text:

```
        # the list's path and the download command (R-400).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
```

New text:

```
        # the list's path and the download command (R-400).
        emits=frozenset({"plan"}), output_schema="plan/1",
```

### `u72.M8_registry_digest_source`

The registry gate declares no digest source

- File: `src/cratekit/cli/registry.py`
- Source: `u72.json`, row `M8_registry_digest_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[a file arrived]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[batch name]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[export]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[folder]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
                prompt="Move these files into the library and write the intake file?",
                digest_source="plan",
```

New text:

```
                prompt="Move these files into the library and write the intake file?",
```

### `u91.G1_registry_xml`

registry route.unplaced: declare no write surface, so doctor and conformance 8 no longer see the xml write

- File: `src/cratekit/cli/registry.py`
- Source: `u91.json`, row `G1_registry_xml`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; route.unplaced's xml write surface is the same value, dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`
- Collected: 1216 against a baseline of 1216
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_declares_no_write_and_needs_only_what_a_read_needs`

Old text:

```
        writes=frozenset({"xml"}), taxonomy_terms=("genre_energy",),
```

New text:

```
        taxonomy_terms=("genre_energy",),
```

### `u96-b.B1_no_library_check_declared`

registry: declare library.mounted on the recovery verb, a check it needs to FAIL

- File: `src/cratekit/cli/registry.py`
- Source: `u96-b.json`, row `B1_no_library_check_declared`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; restore.bare-metal's checks are the same tuple, library.mounted added the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 1113 against a baseline of 1113
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_the_recovery_verb_declares_no_gate_and_no_check_it_needs_to_fail`

Old text:

```
        doctor_checks=("rekordbox.closed",),
        # U96, a verb
```

New text:

```
        doctor_checks=("rekordbox.closed", "library.mounted"),
        # U96, a verb
```

### `r722-b.T6_field_failure_swallowed`

An undecodable field reads as absent in the checked reader, rerun after the fix round

- File: `src/cratekit/core/tags.py`
- Source: `r722-b.json`, row `T6_field_failure_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2982 against a baseline of 2982
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read_and_reads_as_none_beside_its_neighbours`

Old text:

```
            if strict:
                raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

New text:

```
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

### `r722-b.T7_lenient_field_raises`

The lenient reader raises on one undecodable field instead of reading it as None, rerun after the fix round

- File: `src/cratekit/core/tags.py`
- Source: `r722-b.json`, row `T7_lenient_field_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2982 against a baseline of 2982
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read_and_reads_as_none_beside_its_neighbours`

Old text:

```
            if strict:
                raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

New text:

```
            raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
```

### `r722.T1_checked_is_lenient`

read_tags_checked runs the lenient body

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T1_checked_is_lenient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2982 against a baseline of 2982
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read_and_reads_as_none_beside_its_neighbours`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    return _read_tags(path, fields, strict=True)
```

New text:

```
    return _read_tags(path, fields, strict=False)
```

### `r722.T3_open_failure_is_absent`

A mutagen open failure reads as absent in the checked reader

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T3_open_failure_is_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2982 against a baseline of 2982
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        log.debug("tag read failed for %s: %s", path, exc)
```

### `r722.T8_lenient_energy_raises`

read_energy_from_file stops folding a failed read into None

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T8_lenient_energy_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2982 against a baseline of 2982
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None
```

New text:

```
    return read_energy_checked(path)
```

### `r722.T9_lenient_open_raises`

The lenient reader raises when mutagen cannot open a file

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T9_lenient_open_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2982 against a baseline of 2982
- Kills: 305 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_match_states.py::test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - ... and 290 more, see the JSON sidecar

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
```

### `u23-round-8-independent-hunt.HUNT_a_container_leaves_the_writers_table`

Drop .aifc from AIFF_SUFFIXES, so it leaves tags._DIALECT_BY_SUFFIX and LEDGER_CONTAINERS with it

- File: `src/cratekit/core/tags.py`
- Source: `u23-round-8-independent-hunt.json`, row `HUNT_a_container_leaves_the_writers_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 628 against a baseline of 666
- Kills: 1 (collect-error)
- Note: collection changed: 628 collected against a baseline of 666. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_tags.py::test_each_container_is_classified_once[.aifc-Dialect.ID3]`

Old text:

```
AIFF_SUFFIXES = (".aiff", ".aif", ".aifc")
```

New text:

```
AIFF_SUFFIXES = (".aiff", ".aif")
```

### `u23-round-8-independent.X15_save_drops_the_id3v1_trailer`

A tag write destroys an mp3's legacy ID3v1 trailer

- File: `src/cratekit/core/tags.py`
- Source: `u23-round-8-independent.json`, row `X15_save_drops_the_id3v1_trailer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 854 against a baseline of 854
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_mp3s_legacy_id3v1_genre_survives_a_write_and_a_revert[.mp3]`

Old text:

```
    trailer = _id3v1_trailer(path)
    handle.save()
    if trailer is not None:
        _restore_id3v1_trailer(path, trailer)

```

New text:

```
    handle.save()

```

### `u240.M25_copyright_key_wrong`

FIELDS: read the MP4 copyright line from a key the downloader never writes

- File: `src/cratekit/core/tags.py`
- Source: `u240.json`, row `M25_copyright_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_folder_copyright.py`, `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`
- Collected: 337 against a baseline of 337
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_folder_copyright.py::test_the_copyright_line_is_read_from_the_key_the_downloader_writes[.m4a]`

Old text:

```
    "copyright": TagSpec("copyright", "TCOP", "cprt"),
```

New text:

```
    "copyright": TagSpec("copyright", "TCOP", "\xa9cpy"),
```

### `u249.M15_noting_reader_drops_field_failure`

_read_tags: note no failure for one undecodable field, so a partly failed read is remembered

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M15_noting_reader_drops_field_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 692 against a baseline of 692
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
            if failed is not None:
                failed.append(f"{key}: {type(exc).__name__}: {exc}")
            values[field] = None
```

New text:

```
            values[field] = None
```

### `u249.M16_noting_reader_drops_open_failure`

_read_tags: note no failure for a container mutagen could not open, so a moment's I/O error is remembered

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M16_noting_reader_drops_open_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 692 against a baseline of 692
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
        if failed is not None:
            failed.append(f"{type(exc).__name__}: {exc}")
        return absent
```

New text:

```
        return absent
```

### `u249.M17_noting_reader_drops_unrecognised`

_read_tags: note no failure for a container mutagen did not recognise

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M17_noting_reader_drops_unrecognised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 692 against a baseline of 692
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.m4a]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.ogg]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[zeros.opus]`

Old text:

```
        if failed is not None:
            failed.append("not a container the tag library recognises")
        return absent
```

New text:

```
        return absent
```

### `u249.M18_noting_reader_drops_unsupported`

_read_tags: note no failure for a container this module does not read

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M18_noting_reader_drops_unsupported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 692 against a baseline of 692
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[short.aac]`

Old text:

```
        if failed is not None:
            failed.append(str(exc))
        return absent
```

New text:

```
        return absent
```

### `u249.M19_noting_reader_inverted`

read_tags_noting: report a failed read as whole

- File: `src/cratekit/core/tags.py`
- Source: `u249.json`, row `M19_noting_reader_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_tags.py`, `tests/test_match_states.py`
- Collected: 692 against a baseline of 692
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.m4a]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[empty.ogg]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[short.aac]`
  - `tests/test_library_reads_remembered.py::test_a_container_the_reader_cannot_take_is_absent_and_not_whole[zeros.opus]`
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_the_noting_reader_answers_what_the_lenient_reader_answers_and_says_what_failed`

Old text:

```
    return values, not failed
```

New text:

```
    return values, True
```

### `u250.M5_word_reads_zero`

whole_number: read a stored value that is not a number as 0 rather than None, so a word files in the lowest band

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M5_word_reads_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`

Old text:

```
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return None
```

New text:

```
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
        return 0
```

### `u250.M6_absent_raises`

whole_number: drop the absent check, so an untagged file raises out of read_truth and abandons the derivation

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M6_absent_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 212 against a baseline of 212
- Kills: 20 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_derivation_over_n_files_makes_n_opens`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[empty.flac-]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.aiff-FORM\x00\x00\x00\x04AIFX]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.m4a-\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk\x00\x00\x00\x08junk]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[garbage.mp3-content1]`
  - `tests/test_rebuild_one_open.py::test_a_file_no_open_can_read_reads_three_absent_values[truncated.wav-RIFF$\x00\x00\x00WAVEfmt ]`
  - `tests/test_rebuild_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_rebuild_one_open.py::test_an_unsupported_suffix_reads_absent_and_opens_nothing`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.aiff]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.flac]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.m4a]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.mp3]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.ogg]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[genre-only-.wav]`
  - `tests/test_rebuild_one_open.py::test_one_open_reads_what_the_three_readers_read[untagged-.aiff]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if value is None:
        return None
    try:
        return int(value)
```

New text:

```
    try:
        return int(value)
```

### `u250.M7_energy_word_reads_absent`

read_energy_checked: answer None for a stored energy that is not a number instead of raising, so a damaged file reads as untagged

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M7_energy_word_reads_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_energy.py`, `tests/test_tags.py`, `tests/test_rebuild_one_open.py`, `tests/test_organize_mirror_edits_u227.py`
- Collected: 125 against a baseline of 125
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    if number is None:
        raise TagReadFailed(f"energylevel is not a number: {value!r}")
```

New text:

```
    if number is None:
        return None
```

### `u250.M8_conversion_learns_decimals`

whole_number: read a decimal as its whole part, so 7.0 files at energy 7 where today it reads None

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M8_conversion_learns_decimals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild_one_open.py`, `tests/test_tags.py`, `tests/test_rebuild.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild_one_open.py::test_a_numeric_reading_converts_the_way_the_single_readers_convert`

Old text:

```
    try:
        return int(value)
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
```

New text:

```
    try:
        return int(float(value))
    except ValueError:
        log.debug("non-numeric %s tag on %s: %r", field, path, value)
```

### `u301.T1_refuse_unknown_admits_a_field`

_refuse_unknown: never refuse, so write_tags of bpm writes nothing and answers True

- File: `src/cratekit/core/tags.py`
- Source: `u301.json`, row `T1_refuse_unknown_admits_a_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tags.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_tagging_engine.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_tags.py::test_writing_a_tempo_field_raises_rather_than_returning_false`

Old text:

```
    unknown = set(names) - set(FIELDS)
    if unknown:
```

New text:

```
    unknown = set(names) - set(FIELDS)
    if False:
```

### `u301.T3_rewrite_reports_a_failed_save`

_rewrite: answer True after a failed save, so a write that never reached the file reads as done

- File: `src/cratekit/core/tags.py`
- Source: `u301.json`, row `T3_rewrite_reports_a_failed_save`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tags.py`, `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_tags.py::test_a_write_to_a_missing_file_returns_false`

Old text:

```
        log.debug(failure, path, exc)
        return False
```

New text:

```
        log.debug(failure, path, exc)
        return True
```

### `u301.T4_spec_admits_an_unknown_field`

_spec: answer the genre spec for any name, so a read of an unknown field answers the genre instead of refusing

- File: `src/cratekit/core/tags.py`
- Source: `u301.json`, row `T4_spec_admits_an_unknown_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tags.py`, `tests/test_tagging_engine.py`, `tests/test_library_reads_remembered.py`
- Collected: 150 against a baseline of 150
- Kills: 2 (killed)
- Killed:
  - `tests/test_tags.py::test_one_open_over_an_unknown_field_raises_rather_than_answering_none`
  - `tests/test_tags.py::test_reading_an_unwritable_field_name_raises`

Old text:

```
    spec = FIELDS.get(field)
    if spec is None:
```

New text:

```
    spec = FIELDS.get(field, FIELDS["genre"])
    if spec is None:
```

### `u81-fetch-b.S1_strip_does_nothing`

strip_tags reports success and removes nothing, so an upload's tempo frame survives

- File: `src/cratekit/core/tags.py`
- Source: `u81-fetch-b.json`, row `S1_strip_does_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_strip_tags_empties_an_id3_chunk_inside_a_container_and_keeps_the_audio`

Old text:

```
        handle.delete()
        return True
```

New text:

```
        return True
```

### `r1467.M19_root_unreadable_refuses`

pass_landed: read a library root that cannot be read as a pass that never landed

- File: `src/cratekit/intake/land_cli.py`
- Source: `r1467.json`, row `M19_root_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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

### `u165.L3_filing_tail`

_land_native: never file after the landing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u165.json`, row `L3_filing_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 98 against a baseline of 98
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

### `u188.M5_repeat_kept`

_mapped_back: keep a repeated pair instead of dropping it, so the refusal names the folder pair twice on a drive that never moved

- File: `src/cratekit/intake/land_cli.py`
- Source: `u188.json`, row `M5_repeat_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22808 against a baseline of 22808
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return tuple(
        dict.fromkeys(
            (
                (str(area.staging), str(planned.folder)),
                (str(scratch_target), str(target)),
                stored,
            )
        )
    )
```

New text:

```
    return (
        (str(area.staging), str(planned.folder)),
        (str(scratch_target), str(target)),
        stored,
    )
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

### `u307.R20_land_only_by_default`

land_cli flags table: --land-only stores false, so every landing skips filing unless the flag is given

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R20_land_only_by_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_intake_land_filed.py`
- Collected: 36 against a baseline of 36
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
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_intake_land_rehearse.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_rekordbox_running_or_an_export_on_a_native_tree_is_refused_before_the_gate`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`

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
- Ran: `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`, `tests/test_inbox_analyzed.py`
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
- Collected: 22808 against a baseline of 22808
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
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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
- Collected: 254 against a baseline of 254
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

