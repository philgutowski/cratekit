# Mutation table: u334-replay-after-3

Measured by `scripts/mutate.py` on 2026-11-24 04:55 UTC, branch `HEAD` at `90c0cc08`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23214 collected. pytest invocations for this batch: 356.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:55 UTC for commit `90c0cc0829da`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 92, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23214 against 23214. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u343.M03_untitled_overwrites_a_title` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 324 | 3 | killed |
| `u343.M06_handle_run_no_resume_skip` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 482 | 10 | killed |
| `u344.M12_decoded_whole_unread` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M13_left_out_ignores_slice` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 5 | killed |
| `u344.M14_left_out_ignores_calibration` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M15_left_out_ignores_tag` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M16_any_verb_is_a_run` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M17_unfinished_run_counts` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M18_any_folder_is_this_one` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M19_left_out_still_queued` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 6 | killed |
| `u344.M20_no_op_lost` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 4 | killed |
| `u344.M21_warning_off_payload` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M22_resume_drops_count` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 2 | killed |
| `u344.M7_scored_under_settings_none` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 1 | killed |
| `u344.M8_scored_under_fallback_none` | `src/cratekit/analysis/cli.py` | user | 4 file(s) | 391 | 7 | killed |
| `u344.M4_fingerprint_means_only` | `src/cratekit/analysis/energy.py` | user | 5 file(s) | 497 | 1 | killed |
| `u343.M11_mark_value_empty` | `src/cratekit/analysis/run.py` | user | 4 file(s) | 264 | 9 | killed |
| `r1694.C1_no_warning` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 135 | 3 | killed |
| `r1694.C2_every_note` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 135 | 2 | killed |
| `r1694.C3_no_dedupe` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 135 | 1 | killed |
| `r1694.C4_words_no_next_run` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 135 | 1 | killed |
| `r678-b.B2_drive_for_a_verb_that_did_not_queue` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 293 | 1 | killed |
| `r678-b.B3_narrow_catch` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 293 | 1 | killed |
| `r705-b.S11_spend_line_always_suppressed` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 118 | 5 | killed |
| `r705-b.S12_dispatcher_never_adds_the_spend` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 118 | 5 | killed |
| `u193.M16_continue_job_branch` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M19_parked_outcome` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M20_continue_step_not_written` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 523 | 3 | killed |
| `u193.M21_swallowed_warning_dropped` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M22_warning_said_twice` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M23_calls_floor` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 523 | 1 | killed |
| `u210.R24_continue_run` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 132 | 1 | killed |
| `u211.D1_refusal_keeps_its_run` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1200 | 2 | killed |
| `u211.D2_continue_step_named` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1200 | 2 | killed |
| `u211.D4_only_the_scans_own_refusal_is_kept` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 137 | 1 | killed |
| `u278.M20_report_spends_reserve` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 1200 | 1 | killed |
| `u278.M21_downloads_not_reserve` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 1200 | 2 | killed |
| `u278.M22_no_upfront_refusal` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 180 | 2 | killed |
| `u303.S1_without_keeps_the_second_flag` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 1295 | 1 | killed |
| `u303.S2_without_keeps_the_joined_form` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 1295 | 2 | killed |
| `u303.S3_without_keeps_the_value` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 1295 | 4 | killed |
| `u303.S4_without_run_names_nothing` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 1295 | 1 | killed |
| `u303.S5_without_calls_keeps_the_hour` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 1295 | 1 | killed |
| `r239-b.S5_converge_key_off` | `src/cratekit/cli/converge.py` | user | 7 file(s) | 724 | 2 | killed |
| `r685-b.C1_converge_opens_before_it_reads` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 112 | 1 | killed |
| `r685-b.C2_converge_lets_the_refusal_escape` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 112 | 1 | killed |
| `r372-b.B1_doctor_majority_is_info` | `src/cratekit/cli/doctor_library.py` | user | 3 file(s) | 494 | 2 | killed |
| `r372-b.B2_doctor_minority_fails` | `src/cratekit/cli/doctor_library.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B4_doctor_reads_before_the_volume_checks` | `src/cratekit/cli/doctor_library.py` | user | 3 file(s) | 494 | 1 | killed |
| `u211.C1_doctor_closed_is_a_note` | `src/cratekit/cli/doctor_library.py` | user | 2 file(s) | 463 | 1 | killed |
| `u211.C2_doctor_paths_take_no_copy` | `src/cratekit/cli/doctor_library.py` | user | 3 file(s) | 514 | 1 | killed |
| `r372-b.B5_doctor_opens_the_live_path` | `src/cratekit/cli/doctor_model.py` | user | 3 file(s) | 494 | 5 | killed |
| `r1334.E1_offer_after_compare` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 6 | killed |
| `r1334.E2_stale_compare_dropped` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 17 | killed |
| `r1334.E3_record_binds_no_offer` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 38 | killed |
| `r1334.S1_stale_not_offered` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 10 | killed |
| `r1334.S2_stale_screen_without_plan` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 8 | killed |
| `r1334.S3_offered_ignored` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 10 | killed |
| `r1334.S5_screen_no_shown` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 8 | killed |
| `r1334.S7_screen_no_options` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1152 | 5 | killed |
| `r1349.C1_argv_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 5 | killed |
| `r1349.C2_run_dropped` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 5 | killed |
| `r1349.E2_open_left` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 10 | killed |
| `r1349.E3_offer_unrecorded` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 47 | killed |
| `r1349.N1_guard_gone` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 8 | killed |
| `r1349.N2_any_gate` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 2 | killed |
| `r1349.N6_offer_inverted` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 9 | killed |
| `r1349.R1_reason_open_gate` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 6 | killed |
| `r1349.R2_answer_remedy` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 2 | killed |
| `r1349.R3_waiting_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 3 | killed |
| `r1349.R4_continue_wrong` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 6 | killed |
| `r1349.R5_open_gate_detail` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1233 | 2 | killed |
| `u112.G1_part_unverified` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 213 | 1 | killed |
| `u211.D3_kept_set_is_narrow` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 229 | 1 | killed |
| `u270.H2_run_job_drives_the_batch` | `src/cratekit/cli/handlers.py` | user | 4 file(s) | 290 | 7 | killed |
| `u46-author.H1_binding_removed` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 19 | killed |
| `u46-author.H2_is_known_always_true` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 3 | killed |
| `u46-author.H4_unbound_reason_silent` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 1 | killed |
| `u46-author.H7_no_drift` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 2 | killed |
| `u52-item-derivation.B1_label_import_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 296 | 6 | killed |
| `u52-item-derivation.B2_sync_labels_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 296 | 48 | killed |
| `u52-item-derivation.B3_sync_labels_wrong_worker` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 296 | 42 | killed |
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
| `u239.L02_remember_owner` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.L03_remember_called` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 6 | killed |
| `u239.L05_commands_added` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 3 | killed |
| `u239.L06_unrecorded_warning` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 1 | killed |
| `u303.L1_land_key_wrong` | `src/cratekit/cli/label_sync.py` | user | 2 file(s) | 134 | 60 | killed |
| `u303.L2_tail_not_kept` | `src/cratekit/cli/label_sync.py` | user | 2 file(s) | 134 | 4 | killed |
| `u219.C1_rebuild_items_filtered` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u219.C2_rebuild_named_intake` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 5 | killed |
| `u219.K2_accept_actor` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u219.K3_accept_declined` | `src/cratekit/cli/rebuild.py` | user | 2 file(s) | 77 | 1 | killed |
| `u328.S1_a_part_left_out_of_the_table` | `src/cratekit/cli/registry.py` | user | 92 file(s) | 8498 | collection error | collect-error |
| `u44-author.D1_registry_drops_long_running` | `src/cratekit/cli/registry_modules.py` | maintainer | 22 file(s) | 4232 | collection error | collect-error |
| `r372-b.B12_verb_does_not_declare_the_check` | `src/cratekit/cli/registry_pipeline.py` | user | 3 file(s) | 1488 | 1 | killed |
| `a32.R1_gate_not_explicit` | `src/cratekit/cli/registry_state.py` | user | 2 file(s) | 1080 | 5 | killed |
| `r923.N20_gate_takes_inline_answer` | `src/cratekit/cli/registry_state.py` | user | 1 file(s) | 53 | 5 | killed |
| `u96-b.B1_no_library_check_declared` | `src/cratekit/cli/registry_state.py` | user | 2 file(s) | 1114 | 1 | killed |
| `r424.A1_writes_narrowed` | `src/cratekit/cli/registry_sync.py` | user | 2 file(s) | 1143 | 2 | killed |
| `r424.A2_cloud_gate_absent` | `src/cratekit/cli/registry_sync.py` | user | 2 file(s) | 1143 | 2 | killed |
| `r424.A3_rekordbox_checks` | `src/cratekit/cli/registry_sync.py` | user | 3 file(s) | 1560 | 1 | killed |
| `r424.A4_library_mounted` | `src/cratekit/cli/registry_sync.py` | user | 3 file(s) | 1560 | 1 | killed |
| `r424.A5_summary_both_ways` | `src/cratekit/cli/registry_sync.py` | user | 2 file(s) | 1143 | 1 | killed |
| `r378.G1_drop_the_review_set_case` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 3 | killed |
| `r378.G2_name_is_dumped_with_the_other_fields` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 2 | killed |
| `r378.G3_unresolved_is_omitted` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 4 | killed |
| `r378.G4_the_schema_gate_is_dropped` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 1 | killed |
| `r378.G5_items_are_printed_with_repr` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 3 | killed |
| `r378.G6_the_queue_is_omitted` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 2 | killed |
| `r678-a.A10_proof_ungated_on_verb` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 1 | killed |
| `r678-a.A11_run_count_not_the_total` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 1 | killed |
| `r678-a.A12_retired_file_unnamed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 3 | killed |
| `r678-a.A1_drop_the_job_state_case` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 9 | killed |
| `r678-a.A4_empty_job_id_renders_a_job` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 4 | killed |
| `r678-a.A5_drive_line_for_any_state` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 1 | killed |
| `r678-a.A6_resolution_for_every_job_verb` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 2 | killed |
| `r678-c.A3_after_the_test_fix` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 1 | killed |
| `r682-a.M10_unstated_never_said` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 3 | killed |
| `r682-a.M11_unstated_bound_inclusive` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 3 | killed |
| `r682-a.M12_bool_is_a_count` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 3 | killed |
| `r682-a.M13_zero_reason_printed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `r682-a.M14_no_breakdown_mapping_gate` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `r682-a.M15_no_state_mapping_gate` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `r682-a.M7_reason_line_not_printed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 6 | killed |
| `r682-a.M8_sorted_by_slug_only` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `r682-a.M9_no_tie_break` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `r850-a.E11_queued_gate` | `src/cratekit/cli/render.py` | user | 2 file(s) | 178 | 1 | killed |
| `r850-a.E12_count_gate` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r850-a.E13_row_fallback` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r850-a.E14_line_break_quote` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r850-a.E15_rows_not_printed` | `src/cratekit/cli/render.py` | user | 3 file(s) | 291 | 7 | killed |
| `r856-a.R1_hearted_words` | `src/cratekit/cli/render.py` | user | 2 file(s) | 178 | 3 | killed |
| `r856-a.R2_already_hearted_words` | `src/cratekit/cli/render.py` | user | 2 file(s) | 178 | 3 | killed |
| `r925.R2_string_rows` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r925.R3_no_isrc_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 2 | killed |
| `r925.R5_nameless_row_unsaid` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r925.R6_count_line` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 2 | killed |
| `u169.R1_job_list_ungated` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R2_job_list_not_rendered` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R3_unreadable_reads_as_none` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R4_skipped_count_dropped` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R5_no_worker_dropped` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R6_filter_unnamed` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u97-a.A1_bare_verb_returns` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1611 | 3 | killed |
| `u97-a.A4_procedure_drops_the_flag` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1611 | 4 | killed |
| `u97-a.A5_procedure_drops_the_document` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1611 | 4 | killed |
| `u97-a.A6_remedy_text_drops_the_advice` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1611 | 9 | killed |
| `u97-c.C2_remediation_line_drops_the_token_branch` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1611 | 4 | killed |
| `u27-reports-round-1.S1_limit_floor` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.S2_truncation_row` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S3_summary_total` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S6_lossy_marker` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 3 | killed |
| `u27-reports-round-2.S5_handler_key_wrong` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-3-fixes.F1_as_of_falsiness` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-3-fixes.F5_gap_row_flood` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `r679-a.E2_listing_drops_the_actor` | `src/cratekit/cli/review.py` | user | 3 file(s) | 834 | 1 | killed |
| `r345.B4_offer_not_demand` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1488 | 10 | killed |
| `r372-b.B10_setup_records_a_literal_root` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 3 | killed |
| `r372-b.B11_setup_records_without_asking` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B6_setup_overwrites_a_recorded_map` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B8_setup_aborts_on_a_copy_it_could_not_make` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B9_setup_offers_a_rule_the_root_does_not_need` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 2 | killed |
| `r663-a.M11_setup_never_checks` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M12_setup_stops_on_every_refusal` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 51 | 1 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 217 | 4 | killed |
| `u190.T1_run_folder_absolute` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 1 | killed |
| `u190.T4_name_answers_inline` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 2 | killed |
| `u190.T6_chain_namespace` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 3 | killed |
| `u344.M23_tail_never_passes_flag` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 291 | 3 | killed |
| `u344.M24_tail_forgets_run` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 291 | 3 | killed |
| `u344.M25_tail_no_op_stops` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 291 | 3 | killed |
| `r685-a.L3_a_copy_that_does_not_parse_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 2 file(s) | 130 | 5 | killed |
| `r1114.M9_reason_band_upstream` | `src/cratekit/core/cause.py` | user | 3 file(s) | 1344 | 3 | killed |
| `r1313.N1_any_404_not_nearest` | `src/cratekit/core/cause.py` | user | 5 file(s) | 560 | 5 | killed |
| `r1313.N2_failure_alone` | `src/cratekit/core/cause.py` | user | 5 file(s) | 560 | 14 | killed |
| `r1313.N3_declared_links_only` | `src/cratekit/core/cause.py` | user | 5 file(s) | 560 | 14 | killed |
| `r1313.N4_not_found_status_moved` | `src/cratekit/core/cause.py` | user | 5 file(s) | 560 | 19 | killed |
| `r1313.N5_any_status_is_not_found` | `src/cratekit/core/cause.py` | user | 5 file(s) | 560 | 32 | killed |
| `r1313.W1_walk_no_context` | `src/cratekit/core/cause.py` | user | 4 file(s) | 323 | 25 | killed |
| `r1313.W2_walk_no_refusal_boundary` | `src/cratekit/core/cause.py` | user | 4 file(s) | 323 | 6 | killed |
| `r1313.W3_walk_context_cycle` | `src/cratekit/core/cause.py` | user | 2 file(s) | 89 | 7 | killed |
| `r1313.W4_walk_context_before_cause` | `src/cratekit/core/cause.py` | user | 4 file(s) | 323 | 1 | killed |
| `r1349.R8_exit_code` | `src/cratekit/core/cause.py` | user | 8 file(s) | 1233 | 5 | killed |
| `r172-b.B15_reason_maps_to_ok` | `src/cratekit/core/cause.py` | user | 2 file(s) | 328 | 13 | killed |
| `r342.V12_exit_code` | `src/cratekit/core/cause.py` | user | 1 file(s) | 26 | 1 | killed |
| `r372-a.A9_slug_code` | `src/cratekit/core/cause.py` | user | 3 file(s) | 494 | 4 | killed |
| `r388-c.M14_status_registration_dropped` | `src/cratekit/core/cause.py` | maintainer | 70 file(s) | 8192 | 2 | killed |
| `r388-c.M15_status_code_disagrees` | `src/cratekit/core/cause.py` | maintainer | 70 file(s) | 8192 | 2 | killed |
| `r414.M14_reason_unregistered` | `src/cratekit/core/cause.py` | user | 2 file(s) | 1067 | 6 | killed |
| `r500-c.G13_exit_code` | `src/cratekit/core/cause.py` | user | 2 file(s) | 328 | 10 | killed |
| `u173.M22_suspect_exit` | `src/cratekit/core/cause.py` | user | 1 file(s) | 38 | 2 | killed |
| `u27-restore-cli-author.R3_a_backup_slug_leaves_the_cause_vocabulary` | `src/cratekit/core/cause.py` | user | 2 file(s) | 242 | 3 | killed |
| `u27-restore-cli-independent.I_G1_a_second_backup_slug_takes_the_wrong_status` | `src/cratekit/core/cause.py` | maintainer | 3 file(s) | 471 | 2 | killed |
| `u27-round-8-independent.C13_name_db_top_only` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u43-author-light.R2_undeclared_refusal_slug` | `src/cratekit/core/cause.py` | user | 31 file(s) | 5370 | 6 | killed |
| `u44-author.D2_reason_slug_removed` | `src/cratekit/core/cause.py` | user | 32 file(s) | 5427 | 7 | killed |
| `u45-round-1.V2_summary_slug_undeclared` | `src/cratekit/core/cause.py` | user | 33 file(s) | 5516 | 4 | killed |
| `u67.R5_exit_code` | `src/cratekit/core/cause.py` | user | 1 file(s) | 99 | 4 | killed |
| `r926.G10_no_temporary_allowance` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 135 | 17 | killed |
| `r926.G9_temporary_unresolved` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 23214 | 0 (promoted) | zero |
| `u107-a.S01_record_not_json` | `src/cratekit/core/config.py` | user | 1 file(s) | 95 | 2 | killed |
| `u329.R1_config_remedy_drifts_from_the_canonical_text` | `src/cratekit/core/config.py` | user | 4 file(s) | 1528 | 8 | killed |
| `u193.M13_default_coefficient` | `src/cratekit/core/config_schema.py` | user | 5 file(s) | 523 | 3 | killed |
| `r705-b.S10_infinite_interval_accepted` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 118 | 2 | killed |
| `u193.M11_validation_floor` | `src/cratekit/core/config_validate.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M12_validation_bool` | `src/cratekit/core/config_validate.py` | user | 5 file(s) | 523 | 1 | killed |
| `r1991.C4_both_modes_accepted` | `src/cratekit/core/convergence.py` | maintainer | 1 file(s) | 23214 | 0 (promoted) | zero |
| `u219.M2_disposition_cleared` | `src/cratekit/core/convergence.py` | user | 16 file(s) | 960 | 1 | killed |
| `u329.R2_run_setup_token_text` | `src/cratekit/core/exit_codes.py` | user | 5 file(s) | 1945 | 2 | killed |
| `u329.R3_retry_when_unlocked_token_text` | `src/cratekit/core/exit_codes.py` | user | 5 file(s) | 1945 | 1 | killed |
| `u329.R4_record_rekordbox_pin_token_text` | `src/cratekit/core/exit_codes.py` | user | 5 file(s) | 1945 | 1 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 109 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 29 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 349 | 48 | killed |
| `r390-a.A1_retry_re_arms_unconditionally` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 210 | 5 | killed |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 296 | 9 | killed |
| `r390-a.A5_refusal_drops_the_inner_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 210 | 4 | killed |
| `u270.J2_claim_batch_order` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 165 | 22 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 18 file(s) | 1400 | 122 | killed |
| `u46-round-2.M2_resume_does_not_drive` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 59 | 15 | killed |
| `r380.G5_permanent_failures_still_offer_resume` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 166 | 6 | killed |
| `u193.M14_park_job_id_dropped` | `src/cratekit/core/jobs_drive.py` | user | 5 file(s) | 523 | 1 | killed |
| `u193.M15_park_job_id_overwrites` | `src/cratekit/core/jobs_drive.py` | maintainer | 5 file(s) | 523 | 1 | killed |
| `u270.J3_park_releases_the_batch` | `src/cratekit/core/jobs_drive.py` | user | 3 file(s) | 165 | 4 | killed |
| `u270.J7_raise_is_every_outcome` | `src/cratekit/core/jobs_drive.py` | user | 3 file(s) | 165 | 3 | killed |
| `r669-b.B1_composer_not_sanitized` | `src/cratekit/core/naming.py` | user | 2 file(s) | 134 | 2 | killed |
| `r740-a.N1_no_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 17 | killed |
| `r740-a.N2_no_agreement` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 3 | killed |
| `r740-a.N3_key_compared_raw` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 3 | killed |
| `r740-a.N4_stem_before_title` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 1 | killed |
| `r740-a.N5_no_marker_fill` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 4 | killed |
| `r740-a.N6_current_ignores_filled` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 1 | killed |
| `r740-b.E1_library_name_from_stem` | `src/cratekit/core/naming.py` | user | 4 file(s) | 249 | 8 | killed |
| `u39-author-full.D1_default_pad_reverted` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 16 | killed |
| `u39-author-full.D2_pad_unguarded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 2 | killed |
| `u39-author-full.D3_pad_never_runs` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 17 | killed |
| `u39-author-full.E1_budget_ordering_dropped` | `src/cratekit/core/naming.py` | maintainer | 9 file(s) | 1486 | 1 | killed |
| `u39-author-full.E2_wheel_bound_widened` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 10 | killed |
| `u39-author-full.M1_refusal_reworded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 2 | killed |
| `u39-naming-independent.D2_pad_condition_inverted` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 19 | killed |
| `u39-naming-independent.D3_pad_condition_unreachable` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 17 | killed |
| `u39-naming-independent.D4_fake_pad_no_zero_fill` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 17 | killed |
| `u39-naming-independent.E1_budget_ordering_inverted` | `src/cratekit/core/naming.py` | maintainer | 9 file(s) | 1486 | 2 | killed |
| `u39-naming-independent.M1_refusal_reworded` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 2 | killed |
| `u41-author-full.D1_dedupe_disabled` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 9 | killed |
| `u41-author-full.D2_dedupe_structural_rule_widened` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 8 | killed |
| `u41-naming-independent.D3_endswith_widened_to_containment` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 4 | killed |
| `u41-naming-independent.D6_repeat_widened_to_prefix` | `src/cratekit/core/naming.py` | user | 10 file(s) | 1585 | 2 | killed |

## Zero rows and what they owe

- `u27-round-8-independent.C13_name_db_top_only` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r926.G9_temporary_unresolved` (maintainer facing): maintainer facing, composite not required
- `r1991.C4_both_modes_accepted` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u343.M03_untitled_overwrites_a_title`

_untitled: answer the stem for a file that has a title too, so the run overwrites a title tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M03_untitled_overwrites_a_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_restamp_scored_by.py`
- Collected: 324 against a baseline of 324
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[a-title-kept]`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
    if (tags.read_tag(path, "title") or "").strip():
        return None
```

New text:

```
    if False:
        return None
```

### `u343.M06_handle_run_no_resume_skip`

handle_run: never skip a measured file, so a resume measures and writes every file again

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M06_handle_run_no_resume_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_restamp_scored_by.py`
- Collected: 482 against a baseline of 482
- Kills: 10 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_restamp_scored_by.py::test_a_file_the_run_did_not_score_is_restamped_and_the_rest_left_out`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest`

Old text:

```
    artifacts.discard_rename_evidence(cfg, job, item)
    if already_measured(path, cfg):
```

New text:

```
    artifacts.discard_rename_evidence(cfg, job, item)
    if False:
```

### `u344.M12_decoded_whole_unread`

slice_length: answer an ffmpeg decoded file as unread

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M12_decoded_whole_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_the_slices_length_is_the_headers_or_says_the_file_is_decoded_whole`

Old text:

```
            return DECODED_WHOLE
```

New text:

```
            return None
```

### `u344.M13_left_out_ignores_slice`

scored_in_pass: leave out a file whose slice moved with the run's write

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M13_left_out_ignores_slice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 5 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_file_whose_slice_moved_or_went_unread_with_the_runs_write_is_restamped[moved]`
  - `tests/test_restamp_scored_by.py::test_a_file_whose_slice_moved_or_went_unread_with_the_runs_write_is_restamped[unread-after]`
  - `tests/test_restamp_scored_by.py::test_a_file_whose_slice_moved_or_went_unread_with_the_runs_write_is_restamped[unread-before]`
  - `tests/test_restamp_scored_by.py::test_a_file_whose_slice_moved_or_went_unread_with_the_runs_write_is_restamped[unread]`
  - `tests/test_restamp_scored_by.py::test_a_run_report_short_of_a_scored_level_leaves_its_file_to_the_restamp[slice_held-None]`

Old text:

```
            and report.get(SLICE_HELD) is True

```

New text:

```
(empty)
```

### `u344.M14_left_out_ignores_calibration`

scored_in_pass: leave out a file scored under another calibration

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M14_left_out_ignores_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_every_file_is_restamped_once_the_calibration_changed_since_the_run`

Old text:

```
            and report.get(SCORED_UNDER) == active

```

New text:

```
(empty)
```

### `u344.M15_left_out_ignores_tag`

scored_in_pass: leave out a file whose energy tag moved since the run

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M15_left_out_ignores_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_file_whose_tag_moved_since_the_run_is_restamped`

Old text:

```
        if level is not None and as_level(tags.read_tag(path, "energylevel")) == level:
```

New text:

```
        if level is not None:
```

### `u344.M16_any_verb_is_a_run`

scored_in_pass: take any finished job as the run

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M16_any_verb_is_a_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_job_that_is_not_this_folders_finished_run_leaves_nothing_out_and_says_so[another-verb]`

Old text:

```
    if run.handler_key != RUN_HANDLER_KEY or run.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if run.state is not jobs.JobState.SUCCEEDED:
```

### `u344.M17_unfinished_run_counts`

scored_in_pass: take an unfinished run as the run

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M17_unfinished_run_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_job_that_is_not_this_folders_finished_run_leaves_nothing_out_and_says_so[unfinished]`

Old text:

```
    if run.handler_key != RUN_HANDLER_KEY or run.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if run.handler_key != RUN_HANDLER_KEY:
```

### `u344.M18_any_folder_is_this_one`

scored_in_pass: take a run over another folder

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M18_any_folder_is_this_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_job_that_is_not_this_folders_finished_run_leaves_nothing_out_and_says_so[another-folder]`

Old text:

```
    if _folder_of(str(run.payload.get("folder") or "")) != folder:
```

New text:

```
    if False:
```

### `u344.M19_left_out_still_queued`

analyze_restamp: queue the files it left out as well

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M19_left_out_still_queued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 6 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_file_the_run_did_not_score_is_restamped_and_the_rest_left_out`
  - `tests/test_restamp_scored_by.py::test_a_file_whose_tag_moved_since_the_run_is_restamped`
  - `tests/test_restamp_scored_by.py::test_a_restamp_told_the_run_measures_none_of_the_files_it_scored`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest`

Old text:

```
        items = [item for item in items if item not in left_out]
```

New text:

```
        items = list(items)
```

### `u344.M20_no_op_lost`

analyze_restamp: queue a job of no items when the run scored every file

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M20_no_op_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 4 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_restamp_told_the_run_measures_none_of_the_files_it_scored`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
        if not items:
            return ctx.envelope(
                data=no_job(ALL_SCORED
```

New text:

```
        if False:
            return ctx.envelope(
                data=no_job(ALL_SCORED
```

### `u344.M21_warning_off_payload`

analyze_restamp: keep the left out nothing warning off the payload, so the foreground loses it

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M21_warning_off_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_restamp_driven_in_the_foreground_still_says_it_left_nothing_out`

Old text:

```
            scored_by[PAYLOAD_LEFT_OUT_NOTHING] = why

```

New text:

```
(empty)
```

### `u344.M22_resume_drops_count`

_resume: leave what was left out off the restamp's answer

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M22_resume_drops_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 2 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_file_the_run_did_not_score_is_restamped_and_the_rest_left_out`
  - `tests/test_restamp_scored_by.py::test_a_restamp_driven_in_the_foreground_still_says_it_left_nothing_out`

Old text:

```
            summary.update(left_out_of(job.payload))

```

New text:

```
(empty)
```

### `u344.M7_scored_under_settings_none`

_scored_under: record no calibration for the shipped detector's settings

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M7_scored_under_settings_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_the_shipped_detector_records_the_calibration_its_settings_carry`

Old text:

```
        return None if held is None else energy.fingerprint(held)
```

New text:

```
        return None
```

### `u344.M8_scored_under_fallback_none`

_scored_under: record no calibration under a stand in detector

- File: `src/cratekit/analysis/cli.py`
- Source: `u344.json`, row `M8_scored_under_fallback_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 391 against a baseline of 391
- Kills: 7 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_file_the_run_did_not_score_is_restamped_and_the_rest_left_out`
  - `tests/test_restamp_scored_by.py::test_a_file_whose_tag_moved_since_the_run_is_restamped`
  - `tests/test_restamp_scored_by.py::test_a_restamp_told_the_run_measures_none_of_the_files_it_scored`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest`
  - `tests/test_restamp_scored_by.py::test_the_run_report_names_the_calibration_its_level_was_scored_under`

Old text:

```
    return None if active is None else energy.fingerprint(active)
```

New text:

```
    return None
```

### `u344.M4_fingerprint_means_only`

fingerprint: digest the means alone, so a refit of the cuts or the floor reads as the same calibration

- File: `src/cratekit/analysis/energy.py`
- Source: `u344.json`, row `M4_fingerprint_means_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_warm.py`, `tests/test_energy_one_measure_librosa.py`, `tests/test_analysis_ahead.py`
- Collected: 497 against a baseline of 497
- Kills: 1 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_calibration_fingerprint_is_one_per_calibration_and_moves_with_a_refit`

Old text:

```
    text = json.dumps(dict(mapping), sort_keys=True, separators=(",", ":"))
```

New text:

```
    text = json.dumps(dict(mapping).get("mean"), sort_keys=True, separators=(",", ":"))
```

### `u343.M11_mark_value_empty`

MARK_VALUE: an empty mark, which the writer skips, so no file is ever marked

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M11_mark_value_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`, `tests/test_restamp_scored_by.py`
- Collected: 264 against a baseline of 264
- Kills: 9 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_batch_resume_skips_a_file_carrying_the_mark_and_reads_the_rest`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
MARK_VALUE = "1"
```

New text:

```
MARK_VALUE = ""
```

### `r1694.C1_no_warning`

dispatcher: never add the warning, so a verb whose login failed to store says nothing

- File: `src/cratekit/cli/__init__.py`
- Source: `r1694.json`, row `C1_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
    envelope = _with_unstored(envelope, unstored_before)

```

New text:

```
(empty)
```

### `r1694.C2_every_note`

_with_unstored: read every note the process holds, so an earlier verb's failure is reported on every later verb

- File: `src/cratekit/cli/__init__.py`
- Source: `r1694.json`, row `C2_every_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`

Old text:

```
    met = module.unstored()[before:]
```

New text:

```
    met = module.unstored()[:]
```

### `r1694.C3_no_dedupe`

_with_unstored: name a class once per failure, so two failures of one class repeat it

- File: `src/cratekit/cli/__init__.py`
- Source: `r1694.json`, row `C3_no_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
({', '.join(dict.fromkeys(met))})
```

New text:

```
({', '.join(met)})
```

### `r1694.C4_words_no_next_run`

_with_unstored: reword the warning so it no longer says the next run logs in again

- File: `src/cratekit/cli/__init__.py`
- Source: `r1694.json`, row `C4_words_no_next_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`

Old text:

```
so the next run logs in again from 
```

New text:

```
so a later run signs in afresh from 
```

### `r678-b.B2_drive_for_a_verb_that_did_not_queue`

job show and job resume name a second driver for a queued job

- File: `src/cratekit/cli/__init__.py`
- Source: `r678-b.json`, row `B2_drive_for_a_verb_that_did_not_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_verb_showing_a_queued_job_it_did_not_queue_names_no_drive`

Old text:

```
        if registry.by_handler_key(job.handler_key).name != envelope.verb:
            return None

```

New text:

```
(empty)
```

### `r678-b.B3_narrow_catch`

a builder raising anything but a refusal escapes as a traceback over a queued job

- File: `src/cratekit/cli/__init__.py`
- Source: `r678-b.json`, row `B3_narrow_catch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_builder_that_raises_leaves_the_queued_verb_a_success`

Old text:

```
    except Exception:  # noqa: BLE001 - see the docstring, a success stays a success
```

New text:

```
    except CratekitError:
```

### `r705-b.S11_spend_line_always_suppressed`

the spend line is never put on the envelope

- File: `src/cratekit/cli/__init__.py`
- Source: `r705-b.json`, row `S11_spend_line_always_suppressed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_the_spend_line_reaches_a_person_on_the_human_output`

Old text:

```
    if spent.calls == 0:
        return envelope

```

New text:

```
    if spent.calls >= 0:
        return envelope

```

### `r705-b.S12_dispatcher_never_adds_the_spend`

the dispatcher emits the verb's envelope without the spend

- File: `src/cratekit/cli/__init__.py`
- Source: `r705-b.json`, row `S12_dispatcher_never_adds_the_spend`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_the_spend_line_reaches_a_person_on_the_human_output`

Old text:

```
    envelope = _with_provider_spend(envelope, spent_before)

```

New text:

```
    envelope = envelope

```

### `u193.M16_continue_job_branch`

continue_command: never resume the job, so a rerun queues a second job

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M16_continue_job_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-job-resumes-that-job]`

Old text:

```
    if job_id:
        return shlex.join
```

New text:

```
    if False:
        return shlex.join
```

### `u193.M19_parked_outcome`

_dispatched_in_scope: a ceiling stop out of a plain verb reads failed, not blocked

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M19_parked_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`

Old text:

```
        parked = isinstance(exc, JobBlocked) or ceiling_stop
```

New text:

```
        parked = isinstance(exc, JobBlocked)
```

### `u193.M20_continue_step_not_written`

_dispatched_in_scope: leave the gate's generic step, so the exact command is never printed

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M20_continue_step_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`

Old text:

```
        if ceiling_stop:
            cause = _with_continue(cause, argv, entry)
```

New text:

```
        if False:
            cause = _with_continue(cause, argv, entry)
```

### `u193.M21_swallowed_warning_dropped`

_dispatched: say nothing when a verb swallowed the stop

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M21_swallowed_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`

Old text:

```
    if stopped is not None and not reported:
```

New text:

```
    if False:
```

### `u193.M22_warning_said_twice`

_dispatched: warn even over a blocked ceiling refusal, so the stop is said twice

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M22_warning_said_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`

Old text:

```
    if stopped is not None and not reported:
```

New text:

```
    if stopped is not None:
```

### `u193.M23_calls_floor`

_positive_calls: accept zero on the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M23_calls_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_calls_that_is_not_a_positive_whole_number_is_a_usage_error[0]`

Old text:

```
    if value < 1:
        raise argparse.ArgumentTypeError
```

New text:

```
    if value < 0:
        raise argparse.ArgumentTypeError
```

### `u210.R24_continue_run`

continue_command: never add the run a cause names

- File: `src/cratekit/cli/__init__.py`
- Source: `u210.json`, row `R24_continue_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_sync_pair_resume.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-run-continues-that-run-once]`

Old text:

```
    run = ["--run", str(run_id)] if run_id and not named else []
```

New text:

```
    run = []
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

### `u211.D4_only_the_scans_own_refusal_is_kept`

dispatcher: keep the run of any refusal carrying the reason, a backup job's summary included, so its printed continue command refuses forever

- File: `src/cratekit/cli/__init__.py`
- Source: `u211.json`, row `D4_only_the_scans_own_refusal_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_scan_jobs.py`, `tests/test_backup_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan_jobs.py::test_a_backup_job_refused_by_the_scan_is_not_offered_as_a_run_to_continue`

Old text:

```
            isinstance(exc, processes.AbsenceUnconfirmed)
            and cause.reason in gates.KEPT_RUN_REASONS
```

New text:

```
            True
            and cause.reason in gates.KEPT_RUN_REASONS
```

### `u278.M20_report_spends_reserve`

spends_reserve: a --report run spends the reserve

- File: `src/cratekit/cli/__init__.py`
- Source: `u278.json`, row `M20_report_spends_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_cli_contract.py`
- Collected: 1200 against a baseline of 1200
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_these_commands_are_classed_by_their_verbs_writes_and_a_report[organize-True-False]`

Old text:

```
    if getattr(args, "report", False):
        return False

```

New text:

```
(empty)
```

### `u278.M21_downloads_not_reserve`

spends_reserve: only an account write spends the reserve, a download does not

- File: `src/cratekit/cli/__init__.py`
- Source: `u278.json`, row `M21_downloads_not_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_cli_contract.py`
- Collected: 1200 against a baseline of 1200
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_these_commands_are_classed_by_their_verbs_writes_and_a_report[acquire.download-False-True]`
  - `tests/test_provider_budget.py::test_these_commands_are_classed_by_their_verbs_writes_and_a_report[label.sync-False-True]`

Old text:

```
    return bool(entry.writes & RESERVE_WRITES)
```

New text:

```
    return bool(entry.writes & frozenset({"remote"}))
```

### `u278.M22_no_upfront_refusal`

dispatcher: drop the --calls refusal before the verb runs

- File: `src/cratekit/cli/__init__.py`
- Source: `u278.json`, row `M22_no_upfront_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`
- Collected: 180 against a baseline of 180
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_the_verb_runs[refused-before-a-verb-that-makes-no-call-runs]`
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_the_verb_runs[the-continue-a-parked-job-prints-is-not-refused-by-its-own-calls]`

Old text:

```
                over = provider_gate.over_the_line(settings)
                if over is not None:
                    raise CratekitError(over)
```

New text:

```
                over = provider_gate.over_the_line(settings)
                if False:
                    raise CratekitError(over)
```

### `u303.S1_without_keeps_the_second_flag`

_without: only the first flag named is taken out, so --calls-per-hour stays in a continue command

- File: `src/cratekit/cli/__init__.py`
- Source: `u303.json`, row `S1_without_keeps_the_second_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`, `tests/test_cli_contract.py`
- Collected: 1295 against a baseline of 1295
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_continue_within_the_configured_hour_names_no_hour`

Old text:

```
        if token in flags:
```

New text:

```
        if token == flags[0]:
```

### `u303.S2_without_keeps_the_joined_form`

_without: a flag given with = is kept

- File: `src/cratekit/cli/__init__.py`
- Source: `u303.json`, row `S2_without_keeps_the_joined_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`, `tests/test_cli_contract.py`
- Collected: 1295 against a baseline of 1295
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-run-that-cannot-continue-starts-anew]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`

Old text:

```
        if token.startswith(tuple(f"{flag}=" for flag in flags)):
```

New text:

```
        if token.startswith(tuple(f"{flag}=" for flag in flags[:0])):
```

### `u303.S3_without_keeps_the_value`

_without: the flag goes and its value stays on the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u303.json`, row `S3_without_keeps_the_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`, `tests/test_cli_contract.py`
- Collected: 1295 against a baseline of 1295
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_continue_within_the_configured_hour_names_no_hour`
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-run-continues-that-run-once]`
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-run-that-cannot-continue-starts-anew]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[spaced]`

Old text:

```
        if token in flags:
            skip = True
```

New text:

```
        if token in flags:
            skip = False
```

### `u303.S4_without_run_names_nothing`

_without_run: a fresh continue keeps the --run it was given

- File: `src/cratekit/cli/__init__.py`
- Source: `u303.json`, row `S4_without_run_names_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`, `tests/test_cli_contract.py`
- Collected: 1295 against a baseline of 1295
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_job_or_run_to_continue[a-run-that-cannot-continue-starts-anew]`

Old text:

```
    return _without(tokens, ("--run",))
```

New text:

```
    return _without(tokens, ("--rerun",))
```

### `u303.S5_without_calls_keeps_the_hour`

_without_calls: --calls-per-hour is no longer taken out before the raised one is added

- File: `src/cratekit/cli/__init__.py`
- Source: `u303.json`, row `S5_without_calls_keeps_the_hour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`, `tests/test_cli_contract.py`
- Collected: 1295 against a baseline of 1295
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_continue_within_the_configured_hour_names_no_hour`

Old text:

```
    return _without(tokens, ("--calls", "--calls-per-hour"))
```

New text:

```
    return _without(tokens, ("--calls",))
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

### `r685-b.C1_converge_opens_before_it_reads`

Converge opens the database before reading the declaration, the order the review found

- File: `src/cratekit/cli/converge.py`
- Source: `r685-b.json`, row `C1_converge_opens_before_it_reads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
            declared = active_taxonomy.load(cfg)
            handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
            handle = rb_writer.open_db(cfg=cfg)
            declared = active_taxonomy.load(cfg)

```

### `r685-b.C2_converge_lets_the_refusal_escape`

The declaration is read outside the try, so a refusal escapes instead of reading NOT COMPARED

- File: `src/cratekit/cli/converge.py`
- Source: `r685-b.json`, row `C2_converge_lets_the_refusal_escape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`
- Collected: 112 against a baseline of 112
- Kills: 1 (killed)
- Killed:
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
        handle = declared = None
        try:
            declared = active_taxonomy.load(cfg)
            handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
        handle = declared = None
        declared = active_taxonomy.load(cfg)
        try:
            handle = rb_writer.open_db(cfg=cfg)

```

### `r372-b.B1_doctor_majority_is_info`

_check_paths_resolved: a majority is a note, so doctor stays green over it

- File: `src/cratekit/cli/doctor_library.py`
- Source: `r372-b.json`, row `B1_doctor_majority_is_info`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_the_two_synthetic_machines_answer_the_check_opposite_ways`

Old text:

```
    if totals.majority_unmapped:
        cause = metadata_cli.majority_unmapped_cause(cfg, totals)
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
```

New text:

```
    if totals.majority_unmapped:
        cause = metadata_cli.majority_unmapped_cause(cfg, totals)
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
```

### `r372-b.B2_doctor_minority_fails`

_check_paths_resolved: a minority refuses, the sitting's own state after the hand edit

- File: `src/cratekit/cli/doctor_library.py`
- Source: `r372-b.json`, row `B2_doctor_minority_fails`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`

Old text:

```
    if totals.unmapped:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
```

New text:

```
    if totals.unmapped:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
```

### `r372-b.B4_doctor_reads_before_the_volume_checks`

_check_paths_resolved: survey a database on a volume the mount checks could not recognise

- File: `src/cratekit/cli/doctor_library.py`
- Source: `r372-b.json`, row `B4_doctor_reads_before_the_volume_checks`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_defers_to_the_volume_checks_before_reading_anything`

Old text:

```
    unreadable = _library_state_unreadable(inputs, "the database")
    if unreadable is not None:
```

New text:

```
    unreadable = _library_state_unreadable(inputs, "the database")
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

### `r372-b.B5_doctor_opens_the_live_path`

_survey_paths: open the configured database itself rather than a copy

- File: `src/cratekit/cli/doctor_model.py`
- Source: `r372-b.json`, row `B5_doctor_opens_the_live_path`
- Moved: the same text, now in src/cratekit/cli/doctor_model.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 5 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_doctor_fails_paths_resolved_over_a_majority_off_a_copy`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_copy_it_could_not_open_as_unknown_rather_than_good`
  - `tests/test_paths_resolved.py::test_doctor_reports_a_minority_as_a_note_and_a_clean_collection_as_ok`
  - `tests/test_paths_resolved.py::test_doctor_reports_an_empty_database_path_under_the_same_cause`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`

Old text:

```
    with rb_writer.read_only_copy(source, cfg=cfg) as db:
        return metadata_cli.resolution_totals(cfg, db)
```

New text:

```
    db = rb_writer.open_db(source, check_app_version=False, cfg=cfg)
    try:
        return metadata_cli.resolution_totals(cfg, db)
    finally:
        rb_writer.close_db(db)
```

### `r1334.E1_offer_after_compare`

require (existing, sampled): record the offer only on the open gate, so the decide after a stale binds the shown digest again and every resume is stale

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E1_offer_after_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 6 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`

Old text:

```
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest
        pins =
```

New text:

```
        if spec.digest_source is not None and digest is not None and recorded is None:
            self.state.offers[spec.name] = digest
        pins =
```

### `r1334.E2_stale_compare_dropped`

require (existing, sampled): never compare a recorded digest, so a moved plan applies

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E2_stale_compare_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 17 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            if against is not None and against != digest:
```

New text:

```
            if False:
```

### `r1334.E3_record_binds_no_offer`

record (existing, sampled): bind no digest, so the decide after a stale applies any plan

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E3_record_binds_no_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 38 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.all]`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
        digest=state.offers.get(spec.name),
    )
    if state.open_gate == spec.name:
```

New text:

```
        digest=None,
    )
    if state.open_gate == spec.name:
```

### `r1334.S1_stale_not_offered`

require: raise the digest stale as a verb's own, offered false, so the refusal carries no screen and the decide after it binds an unshown plan (R-1334 itself)

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S1_stale_not_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 10 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`

Old text:

```
                    spec, self.state.run_id, against, digest, offered=True, context=context
```

New text:

```
                    spec, self.state.run_id, against, digest, offered=False, context=context
```

### `r1334.S2_stale_screen_without_plan`

require: the stale carries the options but not the plan, context dropped

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S2_stale_screen_without_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 8 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`

Old text:

```
                    spec, self.state.run_id, against, digest, offered=True, context=context
```

New text:

```
                    spec, self.state.run_id, against, digest, offered=True, context=None
```

### `r1334.S3_offered_ignored`

DecisionStale: never add the screen, whatever offered says

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S3_offered_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 10 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`

Old text:

```
        if offered:
            detail.update(_screen(spec, context))
```

New text:

```
        if False:
            detail.update(_screen(spec, context))
```

### `r1334.S5_screen_no_shown`

_screen: drop the shown plan, keep the options

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S5_screen_no_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 8 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`

Old text:

```
    if context is not None:
        screen["shown"] = dict(context)
    return screen
```

New text:

```
    return screen
```

### `r1334.S7_screen_no_options`

_screen: no options, so the human screen is never printed for a stale

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S7_screen_no_options`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1152 against a baseline of 1152
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`

Old text:

```
        "options": list(spec.options),
        "prompt": spec.prompt,
```

New text:

```
        "prompt": spec.prompt,
```

### `r1349.C1_argv_ignored`

continue_command: the recorded command line ignored, so every continue says the verb's words and an ellipsis

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `C1_argv_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`

Old text:

```
    if state.argv is not None:
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
```

New text:

```
    if False:
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
```

### `r1349.C2_run_dropped`

continue_command: the --run dropped, so the command starts a fresh run that loses the answers

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `C2_run_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`

Old text:

```
        return shlex.join(["crate", "--run", state.run_id, *state.argv])
```

New text:

```
        return shlex.join(["crate", *state.argv])
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

### `r1349.N1_guard_gone`

record: the not reached refusal removed, so an answer ahead of a digest gate is recorded with no digest (R-1349 itself)

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N1_guard_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 8 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`

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
        False
        and spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N2_any_gate`

record: the digest source clause dropped, so a gate that binds no plan is refused ahead too

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N2_any_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_that_binds_no_plan_takes_an_answer_before_it_is_reached`
  - `tests/test_organize.py::test_a_gate_with_no_digest_source_still_takes_an_answer_before_it_is_reached`

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
        spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N6_offer_inverted`

record: the offer clause inverted, refusing only a gate that holds an offer

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N6_offer_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 9 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_handed_off_run_holds_the_offer_its_decide_binds`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`

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
        and spec.name in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.R1_reason_open_gate`

GateNotReached: reason decision-required, read and printed as an open gate inviting the refused answer

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R1_reason_open_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 6 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`

Old text:

```
                reason="gate-not-reached",
```

New text:

```
                reason="decision-required",
```

### `r1349.R2_answer_remedy`

GateNotReached: carries the answer-decision remedy verbs read as an open gate

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R2_answer_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`

Old text:

```
                remediation=Remediation(steps=steps),
```

New text:

```
                remediation=Remediation(remedy=Remedy.ANSWER_DECISION, steps=steps),
```

### `r1349.R3_waiting_ignored`

GateNotReached: the gate the run waits at is never named in the steps

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R3_waiting_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`

Old text:

```
        if waiting is not None:
            steps: tuple
```

New text:

```
        if False:
            steps: tuple
```

### `r1349.R4_continue_wrong`

GateNotReached: the continue step names a fresh run of the verb instead of the run under --run

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R4_continue_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 6 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`

Old text:

```
        command = continue_command(state)
        waiting = state.open_gate
```

New text:

```
        command = f"crate {state.verb.replace('.', ' ')}"
        waiting = state.open_gate
```

### `r1349.R5_open_gate_detail`

GateNotReached: the detail's open_gate always None

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R5_open_gate_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`

Old text:

```
                    "open_gate": waiting,
```

New text:

```
                    "open_gate": None,
```

### `u112.G1_part_unverified`

hand_off carries any digest a caller names as the part, whatever the answer was given over

- File: `src/cratekit/cli/gates.py`
- Source: `u112.json`, row `G1_part_unverified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_sync_all.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_part_hand_off_refuses_a_digest_the_answer_was_not_given_over`

Old text:

```
            if output.digest_of(document) != recorded.digest or digest not in _strings(document):
```

New text:

```
            if False:
```

### `u211.D3_kept_set_is_narrow`

KEPT_RUN_REASONS: rekordbox-running keeps its run as well

- File: `src/cratekit/cli/gates.py`
- Source: `u211.json`, row `D3_kept_set_is_narrow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
KEPT_RUN_REASONS: tuple[str, ...] = (processes.UNCONFIRMED,)
```

New text:

```
KEPT_RUN_REASONS: tuple[str, ...] = (processes.UNCONFIRMED, "rekordbox-running")
```

### `u270.H2_run_job_drives_the_batch`

run_job: never hand the driver the batch form, so the export goes back to a request a track

- File: `src/cratekit/cli/handlers.py`
- Source: `u270.json`, row `H2_run_job_drives_the_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 290 against a baseline of 290
- Kills: 7 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_worker_naming_a_batch_form_is_driven_in_batches_against_the_frozen_config`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`

Old text:

```
current_config=current, batch=batching
```

New text:

```
current_config=current, batch=None
```

### `u46-author.H1_binding_removed`

Unbind master, so no verb in the build has a handler at all

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H1_binding_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
- Kills: 19 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    "master": "cratekit.master.cli:handle",
```

New text:

```
(empty)
```

### `u46-author.H2_is_known_always_true`

Claim every handler key is bound, including the eighteen that are not

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H2_is_known_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_unbound_verb_says_why_and_every_bound_one_says_nothing`
  - `tests/test_handlers.py::test_is_known_answers_for_a_declared_key_and_an_invented_one`
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`

Old text:

```
    return key in HANDLERS
```

New text:

```
    return True
```

### `u46-author.H4_unbound_reason_silent`

Stop saying why a queued verb has no worker

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H4_unbound_reason_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`

Old text:

```
    return HANDLERS_NOT_YET_BOUND.get(key)
```

New text:

```
    return None
```

### `u46-author.H7_no_drift`

Never compute drift, so a moved configuration is silently chosen between

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H7_no_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between`
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`

Old text:

```
        current: config.Config | None = config.load()
```

New text:

```
        current: config.Config | None = None
```

### `u52-item-derivation.B1_label_import_unbound`

Unbind label.import, leaving a queued job with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Source: `u52-item-derivation.json`, row `B1_label_import_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 6 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`
  - `tests/test_label_workers.py::test_both_label_keys_report_a_bound_worker_rather_than_a_reason_they_have_none`
  - `tests/test_label_workers.py::test_neither_label_key_is_recorded_as_unbound_now_that_both_are_bound`
  - `tests/test_label_workers.py::test_one_worker_serves_both_label_keys`
  - `tests/test_label_workers.py::test_the_keys_this_verb_will_drive_are_the_keys_bound_to_its_worker`

Old text:

```
    "label.import": "cratekit.label.cli:handle",
```

New text:

```
(empty)
```

### `u52-item-derivation.B2_sync_labels_unbound`

Unbind sync.labels, leaving a queued sweep with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Source: `u52-item-derivation.json`, row `B2_sync_labels_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 48 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_catalogue_the_library_already_holds_offers_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent`
  - `tests/test_label_workers.py::test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_refusal_raised_in_kind_keeps_its_own_reason[artist-lookup]`
  - `tests/test_label_workers.py::test_a_refusal_raised_in_kind_keeps_its_own_reason[sweep-verifier]`
  - `tests/test_label_workers.py::test_a_refusal_raised_in_kind_keeps_its_own_reason[track-read]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
    "sync.labels": "cratekit.label.cli:handle",
```

New text:

```
(empty)
```

### `u52-item-derivation.B3_sync_labels_wrong_worker`

Point sync.labels at the favorites worker, which asks whether anything checks the TARGET or only that the key is present

- File: `src/cratekit/cli/handlers.py`
- Source: `u52-item-derivation.json`, row `B3_sync_labels_wrong_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 42 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_catalogue_that_cannot_be_listed_fails_the_item_and_the_job`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_catalogue_the_library_already_holds_offers_nothing`
  - `tests/test_label_workers.py::test_a_label_whose_crawl_listed_nothing_at_all_still_succeeds`
  - `tests/test_label_workers.py::test_a_label_whose_every_release_is_tombstoned_still_succeeds`
  - `tests/test_label_workers.py::test_a_listing_failure_that_is_not_a_rate_limit_stays_permanent`
  - `tests/test_label_workers.py::test_a_mixed_listing_of_tombstoned_and_unconfirmed_releases_is_a_label_with_nothing_new`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_release_listing_no_tracks_and_a_release_that_is_gone_are_both_offered`
  - `tests/test_label_workers.py::test_a_release_the_library_holds_only_in_another_version_is_offered`
  - `tests/test_label_workers.py::test_a_release_with_a_row_the_reader_cannot_read_is_offered`
  - `tests/test_label_workers.py::test_a_release_with_one_track_still_missing_is_offered_beside_one_that_is_held`
  - ... and 27 more, see the JSON sidecar

Old text:

```
    "sync.labels": "cratekit.label.cli:handle",
```

New text:

```
    "sync.labels": "cratekit.favorites.cli:handle",
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

### `u239.L02_remember_owner`

_remember: record on whichever run ran the tail, the round one blocking shape

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L02_remember_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    if owner == ctx.run.run_id:
```

New text:

```
    if True:
```

### `u239.L03_remember_called`

label_sync: never record the landing, so a later go runs the tail again

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L03_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        warnings.extend(_remember(ctx, stop, land))
```

New text:

```
        pass
```

### `u239.L05_commands_added`

_with_commands: never name the tail commands on the go's refusal

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L05_commands_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`

Old text:

```
    land = _land_in(cause.detail) if _GO_ORIGIN in cause.origin else None
```

New text:

```
    land = None
```

### `u239.L06_unrecorded_warning`

_remember: drop the warning when another run's record cannot keep the landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L06_unrecorded_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - see below
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001 - see below
```

### `u303.L1_land_key_wrong`

label_sync: the go's landing is read under the wrong key, so no tail is found

- File: `src/cratekit/cli/label_sync.py`
- Source: `u303.json`, row `L1_land_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land_beside.py`
- Collected: 134 against a baseline of 134
- Kills: 60 (killed)
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
  - ... and 45 more, see the JSON sidecar

Old text:

```
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
```

New text:

```
    land = report.get("landing") if isinstance(report, Mapping) else None
```

### `u303.L2_tail_not_kept`

label_sync: the downloads the go's tail leaves are no longer kept under the job

- File: `src/cratekit/cli/label_sync.py`
- Source: `u303.json`, row `L2_tail_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land_beside.py`
- Collected: 134 against a baseline of 134
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own`
  - `tests/test_label_sync_go.py::test_the_tail_keeps_what_it_left_whichever_way_it_ends`

Old text:

```
            go.keep_tail(cfg, store, job, folder)
```

New text:

```
            pass
```

### `u219.C1_rebuild_items_filtered`

crate rebuild: queue every native tree again, the intake tree included

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `C1_rebuild_items_filtered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_of_every_tree_leaves_the_intake_tree_alone`

Old text:

```
        items = tuple(t for t in tree_items(entries, tree_id) if engine.derivable(declared, t))
```

New text:

```
        items = tuple(t for t in tree_items(entries, tree_id))
```

### `u219.C2_rebuild_named_intake`

crate rebuild --tree inbox: queue it rather than asking the acceptance gate

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `C2_rebuild_named_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_naming_the_intake_tree_refuses_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`
  - `tests/test_resort_scope.py::test_the_routing_tree_stays_marked_after_inbox_is_accepted`

Old text:

```
        if tree_id is not None and not engine.derivable(declared, tree_id):
```

New text:

```
        if False:
```

### `u219.K2_accept_actor`

rebuild accept: record the command line's actor string rather than who answered the gate (R34)

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `K2_accept_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`

Old text:

```
        cfg, declared, tree_id, actor=ctx.gate.state.decisions[spec.name].actor
    )
```

New text:

```
        cfg, declared, tree_id, actor=ctx.args.actor
    )
```

### `u219.K3_accept_declined`

rebuild accept: an abort records the disposition anyway

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `K3_accept_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`, `tests/test_resort_scope.py`
- Collected: 77 against a baseline of 77
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`

Old text:

```
    if option != "accept":
```

New text:

```
    if option == "never":
```

### `u328.S1_a_part_left_out_of_the_table`

ENTRIES: leave the modules part out of the assembly, so adoption, deletion, export and the utilities are not registered

- File: `src/cratekit/cli/registry.py`
- Source: `u328.json`, row `S1_a_part_left_out_of_the_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`, `tests/test_crate_sync_skill.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_docs_current.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_gate_not_reached.py`, `tests/test_gate_siblings.py`, `tests/test_gate_stale_screen.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_import_rules.py`, `tests/test_install_command.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_heard.py`, `tests/test_label_judge.py`, `tests/test_label_playlists.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_pending_units.py`, `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_report_genres.py`, `tests/test_reports_cli.py`, `tests/test_restamp_scored_by.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_run_retire.py`, `tests/test_schedule.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_setup_discogs.py`, `tests/test_sync_all.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_sync_mark.py`, `tests/test_sync_night.py`, `tests/test_sync_removed.py`, `tests/test_sync_removed_gone.py`, `tests/test_sync_unmark.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_tag_guess.py`, `tests/test_tag_remap.py`, `tests/test_tag_rows.py`, `tests/test_tag_second.py`, `tests/test_tag_set.py`, `tests/test_tag_suggest.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_u242_taken.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8498 against a baseline of 8614
- Kills: 499 (collect-error)
- Note: collection changed: 8498 collected against a baseline of 8614. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/modules/test_tools.py::test_every_declared_verb_is_in_the_static_registry`
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_workflow_name_and_the_registry_verb_name_cannot_drift`
  - `tests/test_adopt_move.py::test_a_cancelled_move_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_failure_in_the_additions_writes_nothing_at_all`
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`
  - `tests/test_adopt_move.py::test_a_job_carrying_no_plan_is_refused_rather_than_driven`
  - `tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero`
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - ... and 484 more, see the JSON sidecar

Old text:

```
    *MODULE_VERBS,

```

New text:

```
(empty)
```

### `u44-author.D1_registry_drops_long_running`

Remove long_running from the master entry, which should shrink two derived populations

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u44-author.json`, row `D1_registry_drops_long_running`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4232 against a baseline of 4233
- Kills: 2 (collect-error)
- Note: collection changed: 4232 collected against a baseline of 4233. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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

### `r372-b.B12_verb_does_not_declare_the_check`

registry: the My Tags verb stops declaring library.paths_resolved

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `r372-b.json`, row `B12_verb_does_not_declare_the_check`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1488 against a baseline of 1488
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

### `a32.R1_gate_not_explicit`

The confirm gate is answerable inline

- File: `src/cratekit/cli/registry_state.py`
- Source: `a32.json`, row `R1_gate_not_explicit`
- Moved: the same text, now in src/cratekit/cli/registry_state.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`, `tests/test_cli_contract.py`
- Collected: 1080 against a baseline of 1080
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

### `r923.N20_gate_takes_inline_answer`

The repair's gate accepts an inline answer, so a flag on the command writes the rows

- File: `src/cratekit/cli/registry_state.py`
- Source: `r923.json`, row `N20_gate_takes_inline_answer`
- Moved: the same text, now in src/cratekit/cli/registry_state.py, was in src/cratekit/cli/registry.py
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

### `u96-b.B1_no_library_check_declared`

registry: declare library.mounted on the recovery verb, a check it needs to FAIL

- File: `src/cratekit/cli/registry_state.py`
- Source: `u96-b.json`, row `B1_no_library_check_declared`
- Moved: the same text, now in src/cratekit/cli/registry_state.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 1114 against a baseline of 1114
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

### `r424.A1_writes_narrowed`

Restore the four local write surfaces the verb never reaches

- File: `src/cratekit/cli/registry_sync.py`
- Source: `r424.json`, row `A1_writes_narrowed`
- Moved: the same text, now in src/cratekit/cli/registry_sync.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1143 against a baseline of 1143
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

- File: `src/cratekit/cli/registry_sync.py`
- Source: `r424.json`, row `A2_cloud_gate_absent`
- Moved: U328 moved sync.favorites' entry to the sync part, which does not import the shared gate's name, so the row as written ended in a NameError and broke collection with no death; the same gate is added to the same entry's gates, spelled out as the equal value
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1143 against a baseline of 1143
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
            GateSpec(
                name="write.cloudsync.unreadable", options=("proceed", "abort"),
                prompt="Cloud Library Sync state could not be read; proceed anyway?",
                explicit=True,
            ),
        ),
        # Landed (U33, R-130).
```

### `r424.A3_rekordbox_checks`

Restore both rekordbox doctor checks for a verb that reads an export

- File: `src/cratekit/cli/registry_sync.py`
- Source: `r424.json`, row `A3_rekordbox_checks`
- Moved: the same text, now in src/cratekit/cli/registry_sync.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`, `tests/test_doctor.py`
- Collected: 1560 against a baseline of 1560
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

- File: `src/cratekit/cli/registry_sync.py`
- Source: `r424.json`, row `A4_library_mounted`
- Moved: the same text, now in src/cratekit/cli/registry_sync.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`, `tests/test_doctor.py`
- Collected: 1560 against a baseline of 1560
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

- File: `src/cratekit/cli/registry_sync.py`
- Source: `r424.json`, row `A5_summary_both_ways`
- Moved: the same text, now in src/cratekit/cli/registry_sync.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_outbound_workers.py`
- Collected: 1143 against a baseline of 1143
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

### `r378.G1_drop_the_review_set_case`

the original defect: render never asks for the review set

- File: `src/cratekit/cli/render.py`
- Source: `r378.json`, row `G1_drop_the_review_set_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[empty-names-nothing-offered]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-each-label]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-the-unresolved-count-and-not-an-unconfirmed-imprint]`

Old text:

```
    checks = render_checks(envelope)
    review_set = render_review_set(envelope)
    if envelope.cause is not None:
        lines.append("")
        lines += render_cause(envelope.cause, summary_only=bool(checks))
    lines += checks
    lines += review_set

```

New text:

```
    checks = render_checks(envelope)
    if envelope.cause is not None:
        lines.append("")
        lines += render_cause(envelope.cause, summary_only=bool(checks))
    lines += checks

```

### `r378.G2_name_is_dumped_with_the_other_fields`

a named item is printed as key=value, so the name is not its own line

- File: `src/cratekit/cli/render.py`
- Source: `r378.json`, row `G2_name_is_dumped_with_the_other_fields`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-each-label]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-the-unresolved-count-and-not-an-unconfirmed-imprint]`

Old text:

```
    name = item.get("name")
    if isinstance(name, str) and name:
        return name
    return ", ".join(f"{k}={_shown_value(v)}" for k, v in item.items())

```

New text:

```
    return ", ".join(f"{k}={_shown_value(v)}" for k, v in item.items())

```

### `r378.G3_unresolved_is_omitted`

the unresolved count is never printed

- File: `src/cratekit/cli/render.py`
- Source: `r378.json`, row `G3_unresolved_is_omitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_review_set_item_without_a_name_is_rendered_from_its_own_fields`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[empty-names-nothing-offered]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-each-label]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-the-unresolved-count-and-not-an-unconfirmed-imprint]`

Old text:

```
    if unresolved is not None:
        lines.append(f"  unresolved: {_shown_value(unresolved)}")

```

New text:

```
(empty)
```

### `r378.G4_the_schema_gate_is_dropped`

any envelope that carries items is rendered as a review set

- File: `src/cratekit/cli/render.py`
- Source: `r378.json`, row `G4_the_schema_gate_is_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_review_set_rendering_is_gated_on_the_schema_not_an_items_key`

Old text:

```
    if not envelope.schema.startswith("review_set/"):
        return []

```

New text:

```
(empty)
```

### `r378.G5_items_are_printed_with_repr`

each item is the interpreter's spelling, not the name line

- File: `src/cratekit/cli/render.py`
- Source: `r378.json`, row `G5_items_are_printed_with_repr`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_review_set_item_without_a_name_is_rendered_from_its_own_fields`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-each-label]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-the-unresolved-count-and-not-an-unconfirmed-imprint]`

Old text:

```
            lines.append(f"  {_review_item_line(item)}")

```

New text:

```
            lines.append(f"  {item!r}")

```

### `r378.G6_the_queue_is_omitted`

the queue is never named, so an empty harvest looks like no renderer

- File: `src/cratekit/cli/render.py`
- Source: `r378.json`, row `G6_the_queue_is_omitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`
- Collected: 82 against a baseline of 82
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[empty-names-nothing-offered]`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label[names-each-label]`

Old text:

```
    if queue not in (None, ""):
        lines.append(f"  queue: {_shown_value(queue)}")

```

New text:

```
(empty)
```

### `r678-a.A10_proof_ungated_on_verb`

every plan verb's items are rendered as import proof lines

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A10_proof_ungated_on_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_import_proof_is_gated_on_the_verb_as_well_as_the_schema`

Old text:

```
    if not envelope.schema.startswith("plan/") or envelope.verb != "intake.imported":
```

New text:

```
    if not envelope.schema.startswith("plan/"):
```

### `r678-a.A11_run_count_not_the_total`

the proven run count is recounted rather than read from the verb's total

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A11_run_count_not_the_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_proven_run_count_is_the_verbs_own_total`

Old text:

```
    runs = runs if isinstance(runs, int) else len(proven)
```

New text:

```
    runs = len(proven)
```

### `r678-a.A12_retired_file_unnamed`

the retired intake file's name is dropped from the proof line

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A12_retired_file_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_render_payloads.py::test_each_proof_action_is_worded_and_an_unknown_one_keeps_its_fields[item2-  run s: proven earlier; intake file retired to g.xml.imported; run closed]`
  - `tests/test_render_payloads.py::test_the_import_proof_is_gated_on_the_verb_as_well_as_the_schema`

Old text:

```
    filed = f"intake file retired to {PurePath(str(retired)).name}" if retired else None
```

New text:

```
    filed = None
```

### `r678-a.A1_drop_the_job_state_case`

the original defect for the three queueing verbs: render never asks for the job

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A1_drop_the_job_state_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 9 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_render_payloads.py::test_a_builder_that_raises_leaves_the_queued_verb_a_success`
  - `tests/test_render_payloads.py::test_a_verb_showing_a_queued_job_it_did_not_queue_names_no_drive`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_prints_the_settled_job_and_no_drive_command`

Old text:

```
    lines += render_job_state(envelope, drive=drive)

```

New text:

```
(empty)
```

### `r678-a.A4_empty_job_id_renders_a_job`

a queue that held nothing prints a job line with an empty identifier

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A4_empty_job_id_renders_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_empty_playlist_queues_nothing_and_says_so`
  - `tests/test_render_payloads.py::test_an_empty_job_id_is_a_queue_that_held_nothing_and_renders_nothing`
  - `tests/test_render_payloads.py::test_the_job_list_case_belongs_to_the_listing_alone`
  - `tests/test_tag_workers.py::test_a_folder_with_nothing_to_tag_names_no_job`

Old text:

```
    if not isinstance(job_id, str) or not job_id:
        return []
```

New text:

```
    if not isinstance(job_id, str):
        return []
```

### `r678-a.A5_drive_line_for_any_state`

a handed in drive is printed for a job that is no longer queued

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A5_drive_line_for_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_job_that_is_not_queued_names_no_drive_even_when_handed_one`

Old text:

```
    if state == "queued" and drive:
```

New text:

```
    if drive:
```

### `r678-a.A6_resolution_for_every_job_verb`

the intake resolution counts print under any job_state verb

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A6_resolution_for_every_job_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 2 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_reasons_belong_to_the_intake_verbs_alone`
  - `tests/test_render_payloads.py::test_the_resolution_counts_belong_to_the_intake_verbs_alone`

Old text:

```
    if envelope.verb in _RESOLVING_VERBS and state != "queued":
```

New text:

```
    if state != "queued":
```

### `r678-c.A3_after_the_test_fix`

the job case renders any schema whose data carries a job id

- File: `src/cratekit/cli/render.py`
- Source: `r678-c.json`, row `A3_after_the_test_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_job_case_is_gated_on_the_schema_not_a_job_id_key`

Old text:

```
    if not envelope.schema.startswith("job_state/"):
        return []
```

New text:

```
    if False:
        return []
```

### `r682-a.M10_unstated_never_said`

a breakdown that falls short of its count prints no unstated entry and reads as complete

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M10_unstated_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 3 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[empty]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[no-whole-count]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[partial]`

Old text:

```
    if unstated > 0:
```

New text:

```
    if False:
```

### `r682-a.M11_unstated_bound_inclusive`

a complete breakdown prints unstated 0

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M11_unstated_bound_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[complete]`
  - `tests/test_render_payloads.py::test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug`

Old text:

```
    if unstated > 0:
```

New text:

```
    if unstated >= 0:
```

### `r682-a.M12_bool_is_a_count`

a bool passes the whole number test, so True prints as a count and as a reason

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M12_bool_is_a_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 3 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_bool_is_not_a_count_in_the_resolution`
  - `tests/test_render_payloads.py::test_a_count_this_build_cannot_read_is_left_out_rather_than_shown_as_zero`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[no-whole-count]`

Old text:

```
    return isinstance(value, int) and not isinstance(value, bool)
```

New text:

```
    return isinstance(value, int)
```

### `r682-a.M13_zero_reason_printed`

a reason with a zero count is printed beside the others

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M13_zero_reason_printed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[no-whole-count]`

Old text:

```
        (str(why), n) for why, n in reasons.items() if _whole(n) and n > 0
```

New text:

```
        (str(why), n) for why, n in reasons.items() if _whole(n)
```

### `r682-a.M14_no_breakdown_mapping_gate`

a by_reason that is not a mapping is read as one

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M14_no_breakdown_mapping_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_reasons_an_older_or_malformed_progress_cannot_state_print_no_line[not-a-mapping]`

Old text:

```
    by_reason = progress.get("by_reason")
    if not isinstance(by_reason, Mapping):
        return ""
```

New text:

```
    by_reason = progress.get("by_reason") or {}
```

### `r682-a.M15_no_state_mapping_gate`

a state's reasons that are not a mapping are read as one

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M15_no_state_mapping_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_reasons_an_older_or_malformed_progress_cannot_state_print_no_line[state-not-a-mapping]`

Old text:

```
    reasons = by_reason.get(word)
    if not isinstance(reasons, Mapping):
        return ""
```

New text:

```
    reasons = by_reason.get(word)
    if reasons is None:
        return ""
```

### `r682-a.M7_reason_line_not_printed`

the rendering computes the reasons and never prints the line

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M7_reason_line_not_printed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[complete]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[empty]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[no-whole-count]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[partial]`
  - `tests/test_render_payloads.py::test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug`

Old text:

```
        if reasons:
            lines.append(f"    by reason: {reasons}")
```

New text:

```
        if False:
            lines.append(f"    by reason: {reasons}")
```

### `r682-a.M8_sorted_by_slug_only`

the reasons print in slug order rather than most rows first

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M8_sorted_by_slug_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug`

Old text:

```
    counted.sort(key=lambda pair: (-pair[1], pair[0]))
```

New text:

```
    counted.sort(key=lambda pair: pair[0])
```

### `r682-a.M9_no_tie_break`

reasons with the same count keep the order the mapping held them in rather than slug order

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M9_no_tie_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug`

Old text:

```
    counted.sort(key=lambda pair: (-pair[1], pair[0]))
```

New text:

```
    counted.sort(key=lambda pair: -pair[1])
```

### `r850-a.E11_queued_gate`

render.render_job_state: print the counts for a queued job too, so its zeros read as a finished export

- File: `src/cratekit/cli/render.py`
- Source: `r850-a.json`, row `E11_queued_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_outbound_workers.py`
- Collected: 178 against a baseline of 178
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_queued_export_prints_no_counts_since_it_has_written_nothing_yet`

Old text:

```
    if state != "queued":
        lines += _outbound_lines(progress)
```

New text:

```
    if True:
        lines += _outbound_lines(progress)
```

### `r850-a.E12_count_gate`

render._outbound_lines: print any value under a count word, so a bool or a string reads as counted

- File: `src/cratekit/cli/render.py`
- Source: `r850-a.json`, row `E12_count_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_count_this_build_cannot_read_is_left_out_rather_than_shown_as_zero`

Old text:

```
for word, words in _OUTBOUND_WORDS if _whole(counts.get(word))]
```

New text:

```
for word, words in _OUTBOUND_WORDS if counts.get(word) is not None]
```

### `r850-a.E13_row_fallback`

render._outbound_lines: name a row with no artist and no title by nothing, so the line names no track

- File: `src/cratekit/cli/render.py`
- Source: `r850-a.json`, row `E13_row_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_an_export_answer_counts_and_names_each_track_it_left_out`

Old text:

```
            named = named or f"row {_one_line(row.get('identity') or '?')}"
```

New text:

```
            named = named or ""
```

### `r850-a.E14_line_break_quote`

render._one_line: never quote, so a title holding a line break splits its row in two

- File: `src/cratekit/cli/render.py`
- Source: `r850-a.json`, row `E14_line_break_quote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_an_unmatched_title_holding_a_line_break_stays_on_its_line`

Old text:

```
    if "\n" in text or "\r" in text:
        return json.dumps(text, ensure_ascii=False)
    return text
```

New text:

```
    return text
```

### `r850-a.E15_rows_not_printed`

render._outbound_lines: print the counts and none of the unmatched rows, which is the R-850 answer with its list gone

- File: `src/cratekit/cli/render.py`
- Source: `r850-a.json`, row `E15_rows_not_printed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 291 against a baseline of 291
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`
  - `tests/test_render_payloads.py::test_a_favourites_answer_counts_in_its_own_words_and_names_each_unhearted_row`
  - `tests/test_render_payloads.py::test_an_export_answer_counts_and_names_each_track_it_left_out`
  - `tests/test_render_payloads.py::test_an_unmatched_title_holding_a_line_break_stays_on_its_line`

Old text:

```
            lines.append(f"    unmatched: {named}: {_one_line(row.get('reason') or 'no reason given')}")
```

New text:

```
            pass
```

### `r856-a.R1_hearted_words`

render._OUTBOUND_WORDS: drop the hearted words, so the sweep's line omits what it hearted

- File: `src/cratekit/cli/render.py`
- Source: `r856-a.json`, row `R1_hearted_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_render_payloads.py::test_a_favourites_answer_counts_in_its_own_words_and_names_each_unhearted_row`

Old text:

```
    ("hearted", "hearted"),

```

New text:

```
(empty)
```

### `r856-a.R2_already_hearted_words`

render._OUTBOUND_WORDS: print already hearted in the export's playlist words

- File: `src/cratekit/cli/render.py`
- Source: `r856-a.json`, row `R2_already_hearted_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_render_payloads.py::test_a_favourites_answer_counts_in_its_own_words_and_names_each_unhearted_row`

Old text:

```
    ("already_hearted", "already hearted or hearted before"),
```

New text:

```
    ("already_hearted", "already there or written before"),
```

### `r925.R2_string_rows`

A string under intake_tracks is printed one character per line

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R2_string_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_an_intake_tracks_field_that_is_not_a_list_prints_nothing`

Old text:

```
    rows = progress.get(_INTAKE_TRACKS)
    if not isinstance(rows, Sequence) or isinstance(rows, str):
```

New text:

```
    rows = progress.get(_INTAKE_TRACKS)
    if not isinstance(rows, Sequence):
```

### `r925.R3_no_isrc_unsaid`

A track with no ISRC prints nothing where the ISRC goes

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R3_no_isrc_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/test_render_payloads.py::test_job_show_lists_the_frozen_tracks_and_a_payload_without_them_prints_none`

Old text:

```
        isrc = f"isrc {_one_line(row['isrc'])}" if row.get("isrc") else "no isrc"
```

New text:

```
        isrc = f"isrc {_one_line(row['isrc'])}" if row.get("isrc") else ""
```

### `r925.R5_nameless_row_unsaid`

A row with no artist or title prints an empty name instead of its item

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R5_nameless_row_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_job_show_lists_the_frozen_tracks_and_a_payload_without_them_prints_none`

Old text:

```
        named = named or f"item {_one_line(row.get('item') or '?')}"
```

New text:

```
        named = named or ""
```

### `r925.R6_count_line`

The heading line counts one fewer track than it lists

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R6_count_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/test_render_payloads.py::test_job_show_lists_the_frozen_tracks_and_a_payload_without_them_prints_none`

Old text:

```
    lines = [f"  tracks: {len(rows)}"]
```

New text:

```
    lines = [f"  tracks: {len(rows) - 1}"]
```

### `u169.R1_job_list_ungated`

render_job_list: drop the verb gate, so another verb's job_state with a jobs key reads as a listing

- File: `src/cratekit/cli/render.py`
- Source: `u169.json`, row `R1_job_list_ungated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_the_job_list_case_belongs_to_the_listing_alone`

Old text:

```
    if not envelope.schema.startswith("job_state/") or envelope.verb != _LISTING_VERB:
```

New text:

```
    if not envelope.schema.startswith("job_state/"):
```

### `u169.R2_job_list_not_rendered`

render: never call the listing case, the base's empty answer

- File: `src/cratekit/cli/render.py`
- Source: `u169.json`, row `R2_job_list_not_rendered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_job_list_is_driven_end_to_end_in_the_default_output`

Old text:

```
    lines += render_job_list(envelope)

```

New text:

```
(empty)
```

### `u169.R3_unreadable_reads_as_none`

render_job_list: an unreadable rows list reads as an empty queue

- File: `src/cratekit/cli/render.py`
- Source: `u169.json`, row `R3_unreadable_reads_as_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_listing_progress_this_build_cannot_read_prints_nothing_rather_than_none[progress3]`

Old text:

```
    if rows and not listed:
        return []
```

New text:

```
    if False:
        return []
```

### `u169.R4_skipped_count_dropped`

job line: say nothing of the skipped items

- File: `src/cratekit/cli/render.py`
- Source: `u169.json`, row `R4_skipped_count_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_job_list_says_how_many_tracks_a_succeeded_job_skipped`

Old text:

```
        if _whole(skipped) and skipped:
```

New text:

```
        if False:
```

### `u169.R5_no_worker_dropped`

job line: say nothing when no worker is bound

- File: `src/cratekit/cli/render.py`
- Source: `u169.json`, row `R5_no_worker_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_job_list_says_when_a_verb_has_no_worker_to_run_its_job`

Old text:

```
    if row.get("worker") == "none":
```

New text:

```
    if False:
```

### `u169.R6_filter_unnamed`

render_job_list: an empty filtered listing does not name its states

- File: `src/cratekit/cli/render.py`
- Source: `u169.json`, row `R6_filter_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_render_payloads.py::test_a_filtered_empty_job_list_names_the_states_it_was_filtered_to`

Old text:

```
        within = f" in {state}" if isinstance(state, str) and state and state != "all" else ""
```

New text:

```
        within = ""
```

### `u97-a.A1_bare_verb_returns`

_COMMANDS: offer the bare crate login again, the exact defect R-411 measured, which shadows the advice entirely

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A1_bare_verb_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1611 against a baseline of 1611
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
    Remedy.AUTHENTICATE_PROVIDER: None,
```

New text:

```
    Remedy.AUTHENTICATE_PROVIDER: "crate login",
```

### `u97-a.A4_procedure_drops_the_flag`

_PROVIDER_SESSION_PROCEDURE: name the subcommand without --from-file, so the person is told to run a verb that refuses with no source

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A4_procedure_drops_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1611 against a baseline of 1611
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
    "crate login provider-session --from-file, then erase the plaintext file, which "
```

New text:

```
    "crate login provider-session, then erase the plaintext file, which "
```

### `u97-a.A5_procedure_drops_the_document`

_PROVIDER_SESSION_PROCEDURE: drop the pointer at the document that carries the minting command itself

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A5_procedure_drops_the_document`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1611 against a baseline of 1611
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
    "crate login provider-session --from-file, then erase the plaintext file, which "
    "docs/adapters.md in the project's repository sets out step by step"
```

New text:

```
    "crate login provider-session --from-file, then erase the plaintext file"
```

### `u97-a.A6_remedy_text_drops_the_advice`

remedy_text: read the command table alone, the existing fallback this unit now depends on, so every advice only token renders nothing

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A6_remedy_text_drops_the_advice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1611 against a baseline of 1611
- Kills: 9 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`
  - `tests/test_doctor.py::test_a_module_enabled_without_its_credential_is_reported_with_the_fix`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_grant_path_access_advice_claims_neither_act_over_the_other`
  - `tests/test_doctor.py::test_the_human_rendering_shows_the_checks_rather_than_only_a_status`
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
    return _COMMANDS.get(remedy) or _ADVICE.get(remedy)
```

New text:

```
    return _COMMANDS.get(remedy)
```

### `u97-c.C2_remediation_line_drops_the_token_branch`

composite for B5: drop the remedy branch altogether, so every cause with a token falls to its first step or the exit code's generic summary. Shows what the renderer holds when the precedence between the two holds nothing

- File: `src/cratekit/cli/render.py`
- Source: `u97-c.json`, row `C2_remediation_line_drops_the_token_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1611 against a baseline of 1611
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`
  - `tests/test_label_tidal_catalogue.py::test_the_label_paths_refusal_carries_the_token_that_renders_the_procedure`

Old text:

```
    remedy = cause.remediation.remedy
    if remedy is not None:
        words = remedy_text(remedy)
        if words:
            return f"  fix: {words}"
```

New text:

```
    remedy = cause.remediation.remedy
    if False:
        words = remedy_text(remedy)
        if words:
            return f"  fix: {words}"
```

### `u27-reports-round-1.S1_limit_floor`

Pass the limit through unfloored, so a negative one becomes a slice from the end

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S1_limit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end`

Old text:

```
    limit = max(0, int(ctx.args.limit))
```

New text:

```
    limit = int(ctx.args.limit)
```

### `u27-reports-round-1.S2_truncation_row`

Drop the row that says the list was capped

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S2_truncation_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
    if len(listed) < len(report.uncovered):
        findings.append(
            Finding(
                key="coverage.truncated",
                title="the list above is not the whole answer",
                status=Status.INFO,
                detail=(
                    f"{len(listed)} of {len(report.uncovered)} uncovered tracks "
                    f"are listed; raise the limit to see the rest"
                ),
            )
        )

```

New text:

```
(empty)
```

### `u27-reports-round-1.S3_summary_total`

Derive the summary total from the truncated list, the arithmetic that hides the cap

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S3_summary_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
            "uncovered": len(report.uncovered),
```

New text:

```
            "uncovered": len(listed),
```

### `u27-reports-round-1.S6_lossy_marker`

Build the naming template without the configured lossy marker

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S6_lossy_marker`
- Moved: Anchored where u325-replay-after.json replayed it: U298 folded this template's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked, which it now returns; the plain template here drops the configured marker as before, local to this verb
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_rejected_pair_comes_back_suppressed_rather_than_as_a_question`
  - `tests/test_reports_cli.py::test_a_second_run_re_offers_the_same_item_rather_than_a_second_one`
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`

Old text:

```
    return NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate()
```

### `u27-reports-round-2.S5_handler_key_wrong`

Round 1's S5 was inert because the engine default matched; pass a WRONG key instead

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-2.json`, row `S5_handler_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`
  - `tests/test_reports_cli.py::test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default`

Old text:

```
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
```

New text:

```
            view, store, template=_template(cfg), handler_key="duplicates"
```

### `u27-reports-round-3-fixes.F1_as_of_falsiness`

Restore the falsiness test, so an explicitly empty as-of is read as an absent flag

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F1_as_of_falsiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_an_as_of_that_is_not_a_date_refuses_rather_than_answering_for_today[empty]`

Old text:

```
    if written is None:
```

New text:

```
    if not written:
```

### `u27-reports-round-3-fixes.F5_gap_row_flood`

Render one gap row per declared bucket again when the governed tree is absent

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F5_gap_row_flood`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket`

Old text:

```
    if stats.shape.folders == 0:
```

New text:

```
    if False:
```

### `r679-a.E2_listing_drops_the_actor`

review list: leave the actor out of the listing, so a superseded row shows no rule

- File: `src/cratekit/cli/review.py`
- Source: `r679-a.json`, row `E2_listing_drops_the_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        "option": item.option,
        "actor": item.actor,
    }
```

New text:

```
        "option": item.option,
    }
```

### `r345.B4_offer_not_demand`

_resolve_backup: skip the offer and ask outright, so a silent full profile run refuses

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B4_offer_not_demand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1488 against a baseline of 1488
- Kills: 10 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[prompt]`
  - `tests/test_doctor.py::test_a_declined_offer_still_records_the_flags_that_were_given`
  - `tests/test_doctor.py::test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_asks_for_the_backup_destinations_when_the_module_is_on`
  - `tests/test_doctor.py::test_the_wizard_records_nothing_for_backup_when_the_offer_goes_unanswered`
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`

Old text:

```
    elif missing and not wizard.optional(
```

New text:

```
    elif False and not wizard.optional(
```

### `r372-b.B10_setup_records_a_literal_root`

_propose_prefix_map: write the root as a literal path rather than the token

- File: `src/cratekit/cli/setup.py`
- Source: `r372-b.json`, row `B10_setup_records_a_literal_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 3 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_end_to_end_writes_the_rule_and_ends_on_a_doctor_that_reads_it`
  - `tests/test_paths_resolved.py::test_setup_offers_a_rule_from_the_old_drive_to_where_the_library_now_is[the-root-when-the-old-name-is-recorded-twice]`
  - `tests/test_paths_resolved.py::test_setup_offers_the_rule_from_the_databases_own_drive_names_off_a_copy`

Old text:

```
    spelled = config.LIBRARY_ROOT_TOKEN if target == root else target
```

New text:

```
    spelled = target
```

### `r372-b.B11_setup_records_without_asking`

_propose_prefix_map: adopt the rule, the pin's S2 failure one key over

- File: `src/cratekit/cli/setup.py`
- Source: `r372-b.json`, row `B11_setup_records_without_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_records_nothing_when_the_offer_goes_unanswered`

Old text:

```
    if not wizard.optional(
        f"rekordbox records this library's paths under {base}, and the library is "
```

New text:

```
    if False and not wizard.optional(
        f"rekordbox records this library's paths under {base}, and the library is "
```

### `r372-b.B6_setup_overwrites_a_recorded_map`

_propose_prefix_map: offer over a map already recorded, so a re-run replaces it

- File: `src/cratekit/cli/setup.py`
- Source: `r372-b.json`, row `B6_setup_overwrites_a_recorded_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_leaves_a_recorded_map_alone`

Old text:

```
    if isinstance(recorded, list) and recorded:
```

New text:

```
    if False:
```

### `r372-b.B8_setup_aborts_on_a_copy_it_could_not_make`

_propose_prefix_map: let an OSError from the copy escape the verb before the save

- File: `src/cratekit/cli/setup.py`
- Source: `r372-b.json`, row `B8_setup_aborts_on_a_copy_it_could_not_make`
- Moved: U303 shortened the comment under the clause to one line; the except OSError clause of _propose_prefix_map, the guard this row narrows, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_notes_a_file_it_could_not_copy_rather_than_aborting`

Old text:

```
    except OSError as exc:
        # The copy itself failed; a note, since the answers are not yet saved.
```

New text:

```
    except ZeroDivisionError as exc:
        # The copy itself failed; a note, since the answers are not yet saved.
```

### `r372-b.B9_setup_offers_a_rule_the_root_does_not_need`

_propose_prefix_map: offer a rule for a root already under the recorded drive

- File: `src/cratekit/cli/setup.py`
- Source: `r372-b.json`, row `B9_setup_offers_a_rule_the_root_does_not_need`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_rows_already_sit_where_they_say[the-root-sits-under-the-recorded-drive]`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_rows_already_sit_where_they_say[the-two-drive-names-agree]`

Old text:

```
    if root == base or root.startswith(base + "/"):
```

New text:

```
    if False:
```

### `r663-a.M11_setup_never_checks`

setup no longer asks before it saves, so the wrong file is recorded

- File: `src/cratekit/cli/setup.py`
- Source: `r663-a.json`, row `M11_setup_never_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[empty]`
  - `tests/test_paths_resolved.py::test_setup_refuses_a_database_path_that_is_not_a_library_and_records_nothing[foreign]`

Old text:

```
    _refuse_a_database_that_is_not_one(cfg)

```

New text:

```
(empty)
```

### `r663-a.M12_setup_stops_on_every_refusal`

setup's reason gate is removed, so a damaged library stops the verb rather than going to the notes and doctor

- File: `src/cratekit/cli/setup.py`
- Source: `r663-a.json`, row `M12_setup_stops_on_every_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_setup_leaves_a_damaged_library_to_the_notes_and_doctor`

Old text:

```
        if exc.cause.reason == "library-database-not-rekordbox":
            raise

```

New text:

```
        raise

```

### `u172.C1_tail_skips_guess`

through_name: never run the guess after tag folder

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C1_tail_skips_guess`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp.py::test_the_tail_runs_on_the_absolute_batch_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
        if step == TAG:
            guess(chain, folder, pass_name)
```

New text:

```
        if False:
            guess(chain, folder, pass_name)
```

### `u181.T1_rescore_ignores_unable`

tail.rescore: queue the rescore although the model cannot score here

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T1_rescore_ignores_unable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 217 against a baseline of 217
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_asks_nothing_of_a_model_that_cannot_score`

Old text:

```
    if unable is not None:
        chain.summary["vocal_rescore"] = "skipped"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "skipped"
```

### `u190.T1_run_folder_absolute`

run: trust the folder handed in as absolute

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T1_run_folder_absolute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_chain_runs_on_the_absolute_folder_whatever_it_is_handed`

Old text:

```
    folder = folder.expanduser().absolute()
    chain.summary["staging"] = str(folder)
```

New text:

```
    chain.summary["staging"] = str(folder)
```

### `u190.T4_name_answers_inline`

name_argv: leave name apply's confirm unanswered, so the chain stops at a gate a person running the tail answers on the command line

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T4_name_answers_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_name_apply_has_its_confirm_answered_inline_over_the_absolute_staging_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
    return ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]
```

New text:

```
    return ["name", "apply", "--root", str(folder)]
```

### `u190.T6_chain_namespace`

Chain.check: key every check sync.land whatever the chain, so the go's checks read as a sync pass's

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T6_chain_namespace`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 276 against a baseline of 276
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
                "key": f"{self.namespace}.{step}",
```

New text:

```
                "key": f"sync.land.{step}",
```

### `u344.M23_tail_never_passes_flag`

tail_step: never pass the run's job to the restamp

- File: `src/cratekit/cli/tail.py`
- Source: `u344.json`, row `M23_tail_never_passes_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_intake_land_native.py`, `tests/test_sync_bandcamp.py`
- Collected: 291 against a baseline of 291
- Kills: 3 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest`

Old text:

```
    scored = [SCORED_BY_FLAG, chain.analyzed] if step == RESTAMP and chain.analyzed else []
```

New text:

```
    scored = []
```

### `u344.M24_tail_forgets_run`

tail_step: keep no run job on the chain

- File: `src/cratekit/cli/tail.py`
- Source: `u344.json`, row `M24_tail_forgets_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_intake_land_native.py`, `tests/test_sync_bandcamp.py`
- Collected: 291 against a baseline of 291
- Kills: 3 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest`

Old text:

```
        chain.analyzed = job.job_id
```

New text:

```
        chain.analyzed = None
```

### `u344.M25_tail_no_op_stops`

tail_step: read the restamp's all scored no op as nothing to queue, stopping the chain

- File: `src/cratekit/cli/tail.py`
- Source: `u344.json`, row `M25_tail_no_op_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_intake_land_native.py`, `tests/test_sync_bandcamp.py`
- Collected: 291 against a baseline of 291
- Kills: 3 (killed)
- Killed:
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_leaves_out_every_file_the_run_scored_and_says_so`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
        return
    if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
```

New text:

```
    if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
```

### `r685-a.L3_a_copy_that_does_not_parse_falls_back`

An active copy that fails validation is replaced by the shipped template instead of refused

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L3_a_copy_that_does_not_parse_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_rebuild.py`
- Collected: 130 against a baseline of 130
- Kills: 5 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_breaks_after_a_good_load_refuses`
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-a-taxonomy]`
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-toml]`
  - `tests/test_active_taxonomy.py::test_a_copy_that_does_not_parse_refuses_on_every_load`
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        raise refuse(

```

New text:

```
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return _shipped(cfg.taxonomy.template)
        raise refuse(

```

### `r1114.M9_reason_band_upstream`

REASONS: map label-sync-unlisted to UPSTREAM_UNAVAILABLE rather than PRECONDITION, a realistic nearby band

- File: `src/cratekit/core/cause.py`
- Source: `r1114.json`, row `M9_reason_band_upstream`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`, `tests/test_reserved_causes.py`, `tests/test_cli_contract.py`
- Collected: 1344 against a baseline of 1344
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_next_label_whose_listing_fails_reports_the_failure_in_one_check`
  - `tests/test_label_sync.py::test_next_over_two_labels_neither_listable_refuses_and_says_nothing_new_of_neither`

Old text:

```
        "label-sync-unlisted": ExitCode.PRECONDITION,
```

New text:

```
        "label-sync-unlisted": ExitCode.UPSTREAM_UNAVAILABLE,
```

### `r1313.N1_any_404_not_nearest`

nearest_status: return the first 404 on any link rather than the first status, so a server error met while handling a not found is read as the not found and kept

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N1_any_404_not_nearest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`
- Collected: 560 against a baseline of 560
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_met_while_handling_a_404_is_the_outage_it_says[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_met_while_handling_a_404_is_the_outage_it_says[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_met_while_handling_a_404_is_the_outage_it_says[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_met_while_handling_a_404_is_the_outage_it_says[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_the_nearest_status_is_the_first_the_walk_reaches`

Old text:

```
        status = answered_status(link)
        if status is not None:
            return status
    return None
```

New text:

```
        status = answered_status(link)
        if status == NOT_FOUND_STATUS:
            return status
    return None
```

### `r1313.N2_failure_alone`

nearest_status: read the failure alone, as before R-1313, so a 404 whose body is a page is an outage again at all four readers

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N2_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`
- Collected: 560 against a baseline of 560
- Kills: 14 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_track_the_provider_answers_with_an_error_page[a-404-page-is-permanent-with-no-retry]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`
  - `tests/test_provider_not_found_bodies.py::test_the_nearest_status_is_the_first_the_walk_reaches`

Old text:

```
    for link, _declared in failure_links(exc):
        status = answered_status(link)
```

New text:

```
    for link, _declared in [(exc, True)]:
        status = answered_status(link)
```

### `r1313.N3_declared_links_only`

nearest_status: read a status on declared links only, so the 404 three context links under a decode error is never reached

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N3_declared_links_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`
- Collected: 560 against a baseline of 560
- Kills: 14 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_track_the_provider_answers_with_an_error_page[a-404-page-is-permanent-with-no-retry]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`
  - `tests/test_provider_not_found_bodies.py::test_the_nearest_status_is_the_first_the_walk_reaches`

Old text:

```
        status = answered_status(link)
        if status is not None:
            return status
```

New text:

```
        status = answered_status(link)
        if status is not None and _declared:
            return status
```

### `r1313.N4_not_found_status_moved`

NOT_FOUND_STATUS: 410 rather than 404, so no 404 is a not found through the nearest status

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N4_not_found_status_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`
- Collected: 560 against a baseline of 560
- Kills: 19 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_transient_marker_wins_over_a_status_code`
  - `tests/test_adapter_contract.py::test_only_an_explicit_not_found_classifies_permanent[exc3]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[404]`
  - `tests/test_label_tidal_catalogue.py::test_a_404_status_is_gone_whatever_the_class_is_called`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
NOT_FOUND_STATUS = 404
```

New text:

```
NOT_FOUND_STATUS = 410
```

### `r1313.N5_any_status_is_not_found`

answered_not_found: any status nearest the failure reads as a not found, so an outage is remembered as gone

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N5_any_status_is_not_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`
- Collected: 560 against a baseline of 560
- Kills: 32 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_failed_lookup_is_never_kept_and_the_next_one_asks[outage]`
  - `tests/test_isrc_cache.py::test_a_failed_lookup_is_never_kept_and_the_next_one_asks[rejected-session]`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[500]`
  - `tests/test_isrc_cache.py::test_the_catalogue_never_keeps_a_failure[outage]`
  - `tests/test_isrc_cache.py::test_the_catalogue_never_keeps_a_failure[rejected-session]`
  - `tests/test_label_tidal_catalogue.py::test_an_identifier_holding_the_digits_404_does_not_make_a_rejection_a_withdrawal`
  - `tests/test_outbound_tidal_account.py::test_a_rejected_session_mid_sweep_asks_for_a_login_at_item_scope`
  - `tests/test_outbound_tidal_account.py::test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session`
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_provider_refuses_once_is_retried_once_into_the_same_title`
  - `tests/test_outbound_tidal_account.py::test_a_write_refused_twice_is_the_items_cause_and_is_not_tried_a_third_time`
  - `tests/test_outbound_tidal_account.py::test_a_write_the_provider_refuses_once_is_retried_once_and_lands`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_503_page_climbs_the_ladder`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[500-json-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[500-json-isrc_cache]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    return nearest_status(exc) == NOT_FOUND_STATUS
```

New text:

```
    return nearest_status(exc) is not None
```

### `r1313.W1_walk_no_context`

failure_links, moved to core.cause: walk the declared causes alone, so a 404 or a 401 whose body is a page is an outage again

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `W1_walk_no_context`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_provider_rejection_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 323 against a baseline of 323
- Kills: 25 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_track_the_provider_answers_with_an_error_page[a-404-page-is-permanent-with-no-retry]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`
  - `tests/test_provider_not_found_bodies.py::test_the_nearest_status_is_the_first_the_walk_reaches`
  - `tests/test_provider_rejection_bodies.py::test_a_failure_after_login_that_is_no_rejection_is_a_wait[outage]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
    pending = [one.__context__ for one in reversed(declared)]
```

New text:

```
    pending: list[BaseException | None] = []
```

### `r1313.W2_walk_no_refusal_boundary`

failure_links, moved to core.cause: follow a context link into a product refusal, so a failure met while handling a refusal raised from a 404 is read as a not found

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `W2_walk_no_refusal_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_provider_rejection_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 323 against a baseline of 323
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_failure_met_while_handling_a_refusal_raised_from_a_404_is_not_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_failure_met_while_handling_a_refusal_raised_from_a_404_is_not_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_failure_met_while_handling_a_refusal_raised_from_a_404_is_not_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_failure_met_while_handling_a_refusal_raised_from_a_404_is_not_a_not_found[isrc_cache]`
  - `tests/test_provider_rejection_bodies.py::test_a_failure_after_login_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[outage]`

Old text:

```
        if one is None or id(one) in walked or isinstance(one, CratekitError):
```

New text:

```
        if one is None or id(one) in walked:
```

### `r1313.W3_walk_context_cycle`

failure_links, moved to core.cause: drop the walked check off the declared chain, so a context cycle is walked without end

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `W3_walk_context_cycle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_provider_rejection_bodies.py`
- Collected: 89 against a baseline of 89
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_cyclic_chain_ends_and_is_not_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_cyclic_chain_ends_and_is_not_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_cyclic_chain_ends_and_is_not_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_cyclic_chain_ends_and_is_not_a_not_found[isrc_cache]`
  - `tests/test_provider_rejection_bodies.py::test_a_failure_after_login_that_is_no_rejection_is_a_wait[cyclic]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[cyclic]`
  - `tests/test_provider_rejection_bodies.py::test_the_walk_reaches_every_link_once_with_the_declared_chain_first`

Old text:

```
        if one is None or id(one) in walked or isinstance(one, CratekitError):
```

New text:

```
        if one is None or isinstance(one, CratekitError):
```

### `r1313.W4_walk_context_before_cause`

failure_links, moved to core.cause: off the declared chain take a link's context before its own cause, as before round one's fix, so a wrapper raised from a 404 while handling a 503 is read as the outage

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `W4_walk_context_before_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_provider_rejection_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 323 against a baseline of 323
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
        pending.extend((one.__context__, one.__cause__))
```

New text:

```
        pending.extend((one.__cause__, one.__context__))
```

### `r1349.R8_exit_code`

cause: gate-not-reached exits as decision required, the code a chain reads as an open gate

- File: `src/cratekit/core/cause.py`
- Source: `r1349.json`, row `R8_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1233 against a baseline of 1233
- Kills: 5 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_organize.py::test_an_account_answer_before_its_gate_is_shown_is_refused_and_records_nothing`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`

Old text:

```
        "gate-not-reached": ExitCode.PRECONDITION,
```

New text:

```
        "gate-not-reached": ExitCode.DECISION_REQUIRED,
```

### `r172-b.B15_reason_maps_to_ok`

Map the new reason to a zero exit, so the outcome says failed and the status a script reads says fine

- File: `src/cratekit/core/cause.py`
- Source: `r172-b.json`, row `B15_reason_maps_to_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_reserved_causes.py`
- Collected: 328 against a baseline of 328
- Kills: 13 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_file_gone_after_the_plan_is_named_rather_than_skipped`
  - `tests/test_naming_apply_cli.py::test_a_folder_of_both_kinds_is_renamed_through_the_dispatcher`
  - `tests/test_naming_apply_cli.py::test_a_rename_onto_a_name_another_file_holds_overwrites_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rename_the_filesystem_refuses_is_named_and_leaves_no_claim`
  - `tests/test_naming_apply_cli.py::test_a_row_that_appears_after_the_gate_still_protects_its_file`
  - `tests/test_naming_apply_cli.py::test_a_tag_edited_while_the_gate_waits_is_not_renamed_to_a_name_nobody_saw`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_a_title_tag_that_could_not_be_written_is_named`
  - `tests/test_naming_apply_cli.py::test_an_artist_tag_removed_while_the_gate_waits_holds_the_file`
  - `tests/test_naming_apply_cli.py::test_the_report_over_a_held_identifier_says_to_tag_it`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
        "rename-incomplete": ExitCode.PRECONDITION,
```

New text:

```
        "rename-incomplete": ExitCode.OK,
```

### `r342.V12_exit_code`

Declare the slug under REFUSED_BY_POLICY rather than PRECONDITION

- File: `src/cratekit/core/cause.py`
- Source: `r342.json`, row `V12_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`

Old text:

```
"vocal-calibration-unreadable": ExitCode.PRECONDITION,
```

New text:

```
"vocal-calibration-unreadable": ExitCode.REFUSED_BY_POLICY,
```

### `r372-a.A9_slug_code`

REASONS: the slug exits under library-unreadable rather than precondition

- File: `src/cratekit/core/cause.py`
- Source: `r372-a.json`, row `A9_slug_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_paths_resolved.py`, `tests/test_metadata_cli.py`, `tests/test_doctor.py`
- Collected: 494 against a baseline of 494
- Kills: 4 (killed)
- Killed:
  - `tests/test_paths_resolved.py::test_a_plan_over_a_majority_of_unmapped_rows_fails_with_the_totals_in_the_payload`
  - `tests/test_paths_resolved.py::test_a_refusal_built_from_the_totals_names_the_prefixes_and_the_current_map`
  - `tests/test_paths_resolved.py::test_an_apply_over_a_majority_refuses_the_same_way_and_writes_nothing`
  - `tests/test_paths_resolved.py::test_the_verb_declares_the_check_and_the_slug_is_registered`

Old text:

```
        "library-paths-majority-unresolved": ExitCode.PRECONDITION,
```

New text:

```
        "library-paths-majority-unresolved": ExitCode.LIBRARY_UNREADABLE,
```

### `r388-c.M14_status_registration_dropped`

Remove the slug from core.cause REASONS, the P5 registration beside the reservation

- File: `src/cratekit/core/cause.py`
- Source: `r388-c.json`, row `M14_status_registration_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_listing.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_discovery.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_listdoc.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_uncredited_tombstone.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8192 against a baseline of 8192
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "snapshot-listing-failed": ExitCode.PRECONDITION,

```

New text:

```
(empty)
```

### `r388-c.M15_status_code_disagrees`

Register the slug in core.cause at a code the reservation does not hold

- File: `src/cratekit/core/cause.py`
- Source: `r388-c.json`, row `M15_status_code_disagrees`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_listing.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_discovery.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_listdoc.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_uncredited_tombstone.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8192 against a baseline of 8192
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_where_this_table_and_the_closed_reason_registry_overlap_they_agree`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "snapshot-listing-failed": ExitCode.PRECONDITION,
```

New text:

```
        "snapshot-listing-failed": ExitCode.LIBRARY_UNAVAILABLE,
```

### `r414.M14_reason_unregistered`

Remove rating-scale-unknown from REASONS, so the refusal cannot be built

- File: `src/cratekit/core/cause.py`
- Source: `r414.json`, row `M14_reason_unregistered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_policy.py`, `tests/test_cli_contract.py`
- Collected: 1067 against a baseline of 1067
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_policy.py::test_a_curve_mixing_the_two_scales_is_refused_at_plan_time`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[-1]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[20]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[256]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[50]`
  - `tests/test_metadata_policy.py::test_a_cut_value_on_neither_scale_is_refused_at_plan_time[6]`

Old text:

```
        "rating-scale-unknown": ExitCode.PRECONDITION,

```

New text:

```
(empty)
```

### `r500-c.G13_exit_code`

Map the new reason to LIBRARY_UNREADABLE, the code of the verb's other refusal, though the library read cleanly

- File: `src/cratekit/core/cause.py`
- Source: `r500-c.json`, row `G13_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_reserved_causes.py`
- Collected: 328 against a baseline of 328
- Kills: 10 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`

Old text:

```
        "collection-row-unmapped": ExitCode.PRECONDITION,
```

New text:

```
        "collection-row-unmapped": ExitCode.LIBRARY_UNREADABLE,
```

### `u173.M22_suspect_exit`

cause: analysis-suspect exits 30, so the skill's 27 branch never matches

- File: `src/cratekit/core/cause.py`
- Source: `u173.json`, row `M22_suspect_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_ok_only_on_every_field_equal_and_a_waiting_check`
  - `tests/test_rekordbox_visit_skill.py::test_the_exit_codes_it_branches_on_are_the_check_s`

Old text:

```
        "analysis-suspect": ExitCode.LIBRARY_PREREQUISITE,
```

New text:

```
        "analysis-suspect": ExitCode.PRECONDITION,
```

### `u27-restore-cli-author.R3_a_backup_slug_leaves_the_cause_vocabulary`

Remove one refusal from cause.REASONS, so building its cause raises

- File: `src/cratekit/core/cause.py`
- Source: `u27-restore-cli-author.json`, row `R3_a_backup_slug_leaves_the_cause_vocabulary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 242 against a baseline of 242
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "remote-not-configured": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u27-restore-cli-independent.I_G1_a_second_backup_slug_takes_the_wrong_status`

Give an unconfirmed restore a hard failure status the reservation table does not give it, a different member from the author's row so the derived guard is shown to cover the enum rather than one entry

- File: `src/cratekit/core/cause.py`
- Source: `u27-restore-cli-independent.json`, row `I_G1_a_second_backup_slug_takes_the_wrong_status`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`
- Collected: 471 against a baseline of 471
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_where_this_table_and_the_closed_reason_registry_overlap_they_agree`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "restore-not-confirmed": ExitCode.DECISION_REQUIRED,
```

New text:

```
        "restore-not-confirmed": ExitCode.PRECONDITION,
```

### `u27-round-8-independent.C13_name_db_top_only`

Record the database path on the handed-in exception only, not along the declared chain

- File: `src/cratekit/core/cause.py`
- Source: `u27-round-8-independent.json`, row `C13_name_db_top_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for current in _chain(exc):
        try:
            setattr(current, DATABASE_PATH_ATTRIBUTE, spelled)
        except AttributeError:  # pragma: no cover - defensive
            continue
    return exc
```

New text:

```
    try:
        setattr(exc, DATABASE_PATH_ATTRIBUTE, spelled)
    except AttributeError:  # pragma: no cover - defensive
        pass
    return exc
```

### `u43-author-light.R2_undeclared_refusal_slug`

setbuild-anchor-not-indexed leaves cause.REASONS, so refuse raises UnknownReason at the boundary instead of refusing

- File: `src/cratekit/core/cause.py`
- Source: `u43-author-light.json`, row `R2_undeclared_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5370 against a baseline of 5370
- Kills: 6 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_setbuilder_cli.py::test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[path-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_an_anchor_with_no_camelot_key_is_not_indexed`

Old text:

```
        "setbuild-anchor-not-indexed": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u44-author.D2_reason_slug_removed`

Remove source-missing from the closed reason registry, so the shell's own refusal cannot be built

- File: `src/cratekit/core/cause.py`
- Source: `u44-author.json`, row `D2_reason_slug_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5427 against a baseline of 5427
- Kills: 7 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_empty_recording_and_an_unknown_job_refuse_from_the_vocabulary`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        "source-missing": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u45-round-1.V2_summary_slug_undeclared`

Remove backup-nothing-ran from the registry, so its raise site raises UnknownReason at the boundary

- File: `src/cratekit/core/cause.py`
- Source: `u45-round-1.json`, row `V2_summary_slug_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5516 against a baseline of 5516
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        "backup-nothing-ran": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u67.R5_exit_code`

Map collection-unreadable to PRECONDITION rather than LIBRARY_UNREADABLE

- File: `src/cratekit/core/cause.py`
- Source: `u67.json`, row `R5_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_library_with_cloud_sync_on_refuses_and_names_the_real_cause`
  - `tests/test_naming_apply_cli.py::test_a_missing_database_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_read_that_fails_after_the_open_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_an_unopenable_database_refuses_and_renames_nothing`

Old text:

```
        "collection-unreadable": ExitCode.LIBRARY_UNREADABLE,
```

New text:

```
        "collection-unreadable": ExitCode.PRECONDITION,
```

### `r926.G10_no_temporary_allowance`

The primitives lose the system temporary allowance, the strict rule the review round measured at 101 refusals

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G10_no_temporary_allowance`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 135 against a baseline of 135
- Kills: 17 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root`
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[its-ceiling-names-the-exact-command-that-continues]`
  - `tests/test_provider_gate.py::test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent[the-hours-line-U278]`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_client_session_attaches_the_gate_before_the_login_goes_out`
  - `tests/test_provider_gate.py::test_client_session_with_no_gate_still_paces_at_the_defaults`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[account]`
  - `tests/test_provider_gate.py::test_each_opener_paces_with_the_frozen_configuration[catalogue]`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given[joined]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if system_temporary:
        allowed.append(
```

New text:

```
    if False:
        allowed.append(
```

### `r926.G9_temporary_unresolved`

The system temporary directory is compared as spelled, /var against /private/var on macOS, so every scratch write is refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G9_temporary_unresolved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        allowed.append(Path(tempfile.gettempdir()).resolve())
```

New text:

```
        allowed.append(Path(tempfile.gettempdir()))
```

### `u107-a.S01_record_not_json`

sync_cli.load_record: read a record that is not JSON as an empty one, so every question is asked again and every answer is lost

- File: `src/cratekit/core/config.py`
- Source: `u107-a.json`, row `S01_record_not_json`
- Moved: U298 replaced label/sync_cli.load_record's own JSON read with config.read_json_map over config.read_json; the not JSON refusal is read_json's, and answering absent there makes load_record return its empty record, the same outcome the original return of _empty gave
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync.py::test_a_record_that_cannot_be_read_refuses_rather_than_asking_everything_again`
  - `tests/test_label_sync.py::test_the_labels_sweep_refuses_an_unreadable_record_before_any_login`

Old text:

```
    except ValueError as exc:
        raise unusable("it is not JSON") from exc


def read_json_map(
```

New text:

```
    except ValueError as exc:
        return False, None


def read_json_map(
```

### `u329.R1_config_remedy_drifts_from_the_canonical_text`

config.Remedy is a vocabulary of its own again, its run-setup token spelled differently from the canonical one

- File: `src/cratekit/core/config.py`
- Source: `u329.json`, row `R1_config_remedy_drifts_from_the_canonical_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_reserved_causes.py`
- Collected: 1528 against a baseline of 1528
- Kills: 8 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_an_unconfigured_machine_refuses_with_a_precondition_and_a_remedy`
  - `tests/test_cli_contract.py::test_every_module_declaring_its_own_remedies_stays_inside_one_vocabulary`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`
  - `tests/test_config_update.py::test_two_wizards_answering_one_key_differently_refuse_and_write_nothing`
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_reserved_causes.py::test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package`
  - `tests/test_reserved_causes.py::test_upgrade_cratekit_is_declared_twice_and_this_table_reserves_one_meaning`

Old text:

```
from cratekit.core.exit_codes import Remedy as Remedy

```

New text:

```
from cratekit.core.exit_codes import Remedy as _Canonical

Remedy = __import__("enum").StrEnum("Remedy", {m.name: m.value.replace("run-setup", "run-set-up") for m in _Canonical})

```

### `u193.M13_default_coefficient`

config: halve the default ceiling

- File: `src/cratekit/core/config_schema.py`
- Source: `u193.json`, row `M13_default_coefficient`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_releases.py::test_an_estimate_over_the_call_ceiling_asks_even_under_the_builds_own_line`
  - `tests/test_label_playlists_releases.py::test_the_estimate_is_two_calls_a_release_at_the_configured_pace`
  - `tests/test_provider_gate.py::test_the_ceiling_defaults_to_five_hundred_and_round_trips`

Old text:

```
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 500
```

New text:

```
DEFAULT_PROVIDER_CALLS_PER_COMMAND = 250
```

### `r705-b.S10_infinite_interval_accepted`

an infinite interval passes validation and reaches time.sleep

- File: `src/cratekit/core/config_validate.py`
- Source: `r705-b.json`, row `S10_infinite_interval_accepted`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 118 against a baseline of 118
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_pacing_or_ceiling_number_that_is_not_positive_is_refused_naming_the_key[min_interval_s=inf]`
  - `tests/test_provider_gate.py::test_a_pacing_or_ceiling_number_that_is_not_positive_is_refused_naming_the_key[min_interval_s=nan]`

Old text:

```
        or not math.isfinite(interval)
        or interval <= 0

```

New text:

```
        or interval <= 0

```

### `u193.M11_validation_floor`

_validate_provider: accept zero as a ceiling

- File: `src/cratekit/core/config_validate.py`
- Source: `u193.json`, row `M11_validation_floor`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_pacing_or_ceiling_number_that_is_not_positive_is_refused_naming_the_key[calls_per_command=0]`

Old text:

```
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 1
```

New text:

```
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 0
```

### `u193.M12_validation_bool`

_validate_provider: accept true as a ceiling of one

- File: `src/cratekit/core/config_validate.py`
- Source: `u193.json`, row `M12_validation_bool`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_pacing_or_ceiling_number_that_is_not_positive_is_refused_naming_the_key[calls_per_command=True]`

Old text:

```
        not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling < 1
```

New text:

```
        not isinstance(ceiling, int) or ceiling < 1
```

### `r1991.C4_both_modes_accepted`

record_nodes: accept replace_all and keep_recorded together

- File: `src/cratekit/core/convergence.py`
- Source: `r1991.json`, row `C4_both_modes_accepted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 23214 against a baseline of 23214
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if replace_all and keep_recorded:
```

New text:

```
    if False:
```

### `u219.M2_disposition_cleared`

mark_unconverged: a second restore of the same reason leaves a disposed tree's acceptance standing (round two's second hold)

- File: `src/cratekit/core/convergence.py`
- Source: `u219.json`, row `M2_disposition_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_favorites.py`, `tests/test_organize_inspiration.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_restore.py`, `tests/test_sync_pair_back.py`, `tests/test_tag_rows.py`, `tests/test_tree_writer.py`
- Collected: 960 against a baseline of 960
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`

Old text:

```
            if current.unconverged and current.reason == reason and current.disposition is None:
```

New text:

```
            if current.unconverged and current.reason == reason:
```

### `u329.R2_run_setup_token_text`

the one home's run setup token is spelled differently, which config.Remedy now reads too

- File: `src/cratekit/core/exit_codes.py`
- Source: `u329.json`, row `R2_run_setup_token_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_reserved_causes.py`, `tests/test_doctor.py`, `tests/test_config_update.py`
- Collected: 1945 against a baseline of 1945
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_update.py::test_two_wizards_answering_one_key_differently_refuse_and_write_nothing`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    RUN_SETUP = "run-setup"
```

New text:

```
    RUN_SETUP = "run-set-up"
```

### `u329.R3_retry_when_unlocked_token_text`

the one home's retry when unlocked token is spelled differently, which config.Remedy now reads too

- File: `src/cratekit/core/exit_codes.py`
- Source: `u329.json`, row `R3_retry_when_unlocked_token_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_reserved_causes.py`, `tests/test_doctor.py`, `tests/test_config_update.py`
- Collected: 1945 against a baseline of 1945
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    RETRY_WHEN_UNLOCKED = "retry-when-unlocked"
```

New text:

```
    RETRY_WHEN_UNLOCKED = "retry-when-unlock"
```

### `u329.R4_record_rekordbox_pin_token_text`

the one home's record rekordbox pin token is spelled differently, which config.Remedy now reads too

- File: `src/cratekit/core/exit_codes.py`
- Source: `u329.json`, row `R4_record_rekordbox_pin_token_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_reserved_causes.py`, `tests/test_doctor.py`, `tests/test_config_update.py`
- Collected: 1945 against a baseline of 1945
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    RECORD_REKORDBOX_PIN = "record-rekordbox-pin"
```

New text:

```
    RECORD_REKORDBOX_PIN = "record-rekordbox-pins"
```

### `r290-author.J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J3_closed_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 109 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - ... and 94 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if False and not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r290-author.J4_predicate_narrowed_to_failed`

Narrow the closed predicate to FAILED alone, so a run stopped by a signal is reported through a normal envelope

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J4_predicate_narrowed_to_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 29 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
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
  - ... and 14 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if job.state is JobState.FAILED and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Moved: Anchored where u325-replay-after.json replayed it: U298 replaced the resume tails of tagging.shell.advance, adopt.shell.advance, acquire fallback-fetch and master with core.jobs.resumed, which advance calls; its one raise_for_state call is the mapping each of those four shells made, and tests/test_job_outcome.py names that function as the shared tail. The tests are this row's own plus those of the three rows mapped to it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_adopt_workers.py`, `tests/test_master_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 349 against a baseline of 349
- Kills: 48 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.folder]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
    raise_for_state(job)
    return job, warnings
```

New text:

```
    get  # the mapping call, removed
    return job, warnings
```

### `r390-a.A1_retry_re_arms_unconditionally`

the original defect: retry re-arms every failed item whatever the job cause says

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A1_retry_re_arms_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 210 against a baseline of 210
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
            f"job {job_id} {current.state} with a cause that is not retryable, "
            f"so resuming it cannot succeed and its items were left as they are",
            steps=(
                "inspect each failed item's cause on the job's own record",
                "queue the work again the way it was queued the first time, "
                "once the reason is addressed",
            ),
            origin=("jobs",),
            detail={
                "job_id": job_id,
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )

```

New text:

```
(empty)
```

### `r390-a.A2_retry_refuses_any_closed_job_with_a_cause`

the flag is not read: a cancelled job and a retryable failure are refused too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A2_retry_refuses_any_closed_job_with_a_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_backup_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_jobs.py::test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is not None:
        raise refuse(
            "job-not-retryable",
```

### `r390-a.A5_refusal_drops_the_inner_cause`

the refusal no longer nests the job's own cause, so the item's reason is unreachable

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A5_refusal_drops_the_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 210 against a baseline of 210
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )
```

New text:

```
                **_permanent_reasons_of(current.cause),
            },
        )
```

### `u270.J2_claim_batch_order`

claim_batch: claim the highest ordinals first, so a batch writes its tracks in the reverse of the crate's order

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J2_claim_batch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 165 against a baseline of 165
- Kills: 22 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`
  - `tests/test_jobs_batch.py::test_a_batch_is_claimed_in_ordinal_order_up_to_its_size`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_jobs_batch.py::test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other`
  - `tests/test_jobs_batch.py::test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left`
  - `tests/test_jobs_batch.py::test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs`
  - `tests/test_outbound_export_batches.py::test_a_created_playlist_is_said_once_for_the_batch`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            "ORDER BY ordinal LIMIT ?",
```

New text:

```
            "ORDER BY ordinal DESC LIMIT ?",
```

### `u298.H16_reported_extra_under_progress`

reported: a verb's own detail is dropped from progress

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H16_reported_extra_under_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_refused.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_vocals_cli.py`
- Collected: 1400 against a baseline of 1400
- Kills: 122 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - `tests/intake/test_workers.py::test_queueing_a_set_identifies_it_and_gives_the_driver_one_item_per_track`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - ... and 107 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `u46-round-2.M2_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/core/jobs.py`
- Source: `u46-round-2.json`, row `M2_resume_does_not_drive`
- Moved: U298 replaced master's resume with core.jobs.resumed, which master_recording now calls after its reconcile; the drive inside its is_open branch is the same two lines, so removing it reports the queued job without running any of it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 59 against a baseline of 59
- Kills: 15 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
        _result, warnings = ctx.run_job(store, job)
        job = get(store, job.job_id)
```

New text:

```
        pass
```

### `r380.G5_permanent_failures_still_offer_resume`

the permanent branch still carries the resume-job remedy

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r380.json`, row `G5_permanent_failures_still_offer_resume`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_label_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 6 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[three-items]`
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[two-items]`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`
  - `tests/test_label_workers.py::test_a_sweep_whose_failures_are_permanent_does_not_tell_the_person_to_resume`

Old text:

```
        Remediation(
            steps=(
                "the failed items cannot succeed on resume; inspect each item's cause",
            )
        ),

```

New text:

```
        Remediation(remedy=Remedy.RESUME_JOB),

```

### `u193.M14_park_job_id_dropped`

jobs._parked_cause: do not name the job, so the continue command cannot resume it

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u193.json`, row `M14_park_job_id_dropped`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_ceiling_parks_a_job_and_the_resumed_job_continues`

Old text:

```
    if "job_id" in (cause.detail or {}):
        return cause
```

New text:

```
    if True:
        return cause
```

### `u193.M15_park_job_id_overwrites`

jobs._parked_cause: overwrite a job id the cause already carries

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u193.json`, row `M15_park_job_id_overwrites`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 523 against a baseline of 523
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_park_that_names_its_job_keeps_its_own_job_id`

Old text:

```
    if "job_id" in (cause.detail or {}):
        return cause
```

New text:

```
    if False:
        return cause
```

### `u270.J3_park_releases_the_batch`

drive: ignore a Parked among a batch's outcomes, so the batch is settled as failed and the next batch is the second request into a block

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J3_park_releases_the_batch`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 165 against a baseline of 165
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_park_answered_for_one_item_releases_the_whole_batch`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`

Old text:

```
                if parked is not None:
                    release_claims(store, job_id, driver=driver)
```

New text:

```
                if False:
                    release_claims(store, job_id, driver=driver)
```

### `u270.J7_raise_is_every_outcome`

_batch_outcomes: a raise out of the batch handler fails only the first item, and the rest have no outcome

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J7_raise_is_every_outcome`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_export_batches.py`
- Collected: 165 against a baseline of 165
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_that_fails_every_item_records_the_job_failed_then_raises`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_outbound_workers.py::test_a_job_driven_with_no_adapter_fails_rather_than_reporting_success`

Old text:

```
        return {item.item_id: exc for item in claimed}
```

New text:

```
        return {claimed[0].item_id: exc}
```

### `r669-b.B1_composer_not_sanitized`

G14's composite: drop the one sanitizer, the composer's, now that the copy in _artist is gone, so a slash in a credit reaches the filename

- File: `src/cratekit/core/naming.py`
- Source: `r669-b.json`, row `B1_composer_not_sanitized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 134 against a baseline of 134
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_stem_is_the_rows_and_carries_no_path_separator`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-slash-takes-the-body-form-of-a-segment]`

Old text:

```
        part for part in (sanitize_segment(artist or ""), sanitize_segment(title or "")) if part
```

New text:

```
        part for part in (artist or "", title or "") if part
```

### `r740-a.N1_no_fill`

normalize_spec: never fill a spec field from the stripped head, the R-740 loss itself

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N1_no_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 17 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[01A - 112 - Ain't Gonna Hurt Nobody.flac-fields0-01A - 112 - Ain't Gonna Hurt Nobody-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields4-05B - 98 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[08A - 124 - [MP3] Body.flac-fields8-08A - 124 - [MP3] Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields1-08A - 124 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields2-08A - 124 - Body-3B]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields3-08A - 124 - Body-Am]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-stripped-head-marks-the-spec]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[stem-head-fills-when-title-has-none]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            filled.update(
                (name, value) for name, value in values.items() if current[name] is None
            )
```

New text:

```
            pass
```

### `r740-a.N2_no_agreement`

normalize_spec: fill from the head whatever the spec supplied, so a fresh key takes the old tempo

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N2_no_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[fresh-key-never-paired-with-stale-tempo]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[off-wheel-key-not-completed]`

Old text:

```
        if all(_agrees(name, current[name], values[name]) for name in values):
```

New text:

```
        if True:
```

### `r740-a.N3_key_compared_raw`

_agrees: compare the key as raw text instead of on the wheel, so 8a disagrees with 08A

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N3_key_compared_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 3 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[unpadded-lowercase-key-agrees-with-head]`

Old text:

```
        return parsed is not None and parsed == parse_camelot(str(written))
```

New text:

```
        return str(supplied) == str(written)
```

### `r740-a.N4_stem_before_title`

normalize_spec: read the stem head before the title head

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N4_stem_before_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[title-head-read-before-stem-head]`

Old text:

```
    for head, fields in ((title_head, title_fields), (stem_head, stem_fields)):
```

New text:

```
    for head, fields in ((stem_head, stem_fields), (title_head, title_fields)):
```

### `r740-a.N5_no_marker_fill`

normalize_spec: a marker in the stripped head no longer marks the spec, so R21's marker is dropped

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N5_no_marker_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 4 (killed)
- Killed:
  - `tests/test_landing_head.py::test_the_lossy_flag_reported_is_the_one_the_name_was_rendered_from`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[08A - 124 - [MP3] Body.flac-fields8-08A - 124 - [MP3] Body-None]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-stripped-head-marks-the-spec]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-only-head-invents-no-field]`

Old text:

```
            if rule.literal in head:
                filled[rule.field] = True
```

New text:

```
            if rule.literal in head:
                pass
```

### `r740-a.N6_current_ignores_filled`

normalize_spec: judge the stem head against the spec alone, so it overwrites what the title head filled

- File: `src/cratekit/core/naming.py`
- Source: `r740-a.json`, row `N6_current_ignores_filled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[title-head-read-before-stem-head]`

Old text:

```
        current = {name: filled.get(name, getattr(spec, name)) for name in values}
```

New text:

```
        current = {name: getattr(spec, name) for name in values}
```

### `r740-b.E1_library_name_from_stem`

existing guard sample: render_all derives the library name from the filename stem instead of the title tag

- File: `src/cratekit/core/naming.py`
- Source: `r740-b.json`, row `E1_library_name_from_stem`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming.py`, `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`
- Collected: 249 against a baseline of 249
- Kills: 8 (killed)
- Killed:
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[a-provider-key-tag]`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[titled]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields4-05B - 98 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body [MP3].flac-fields7-Body-None]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[marker-in-body-marks-nothing]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`

Old text:

```
        library_name=title_tag,
```

New text:

```
        library_name=head + spec.stem,
```

### `u39-author-full.D1_default_pad_reverted`

Revert the key_pad default to none, the pre U39 written form

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `D1_default_pad_reverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 16 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[spec-value-wins-over-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[unpadded-lowercase-key-agrees-with-head]`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_budget_head_equals_the_written_head_since_the_pad_moved_in`
  - `tests/test_naming.py::TestRender::test_render[fitted-stem-passes-verbatim]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::TestRender::test_render[stem-is-the-fallback-title]`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::test_a_second_template_produces_a_different_correct_tree_with_no_code_change`
  - `tests/test_naming.py::test_an_optional_field_widens_render_and_parse_together`
  - `tests/test_naming.py::test_the_default_template_writes_the_padded_form[data-case-normalized]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    key_pad: str = "camelot2"

```

New text:

```
    key_pad: str = "none"

```

### `u39-author-full.D2_pad_unguarded`

Pad unconditionally, so an off wheel key raises from pad_camelot instead of the one refusal path

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `D2_pad_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[bare]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[default]`

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "camelot2":

```

### `u39-author-full.D3_pad_never_runs`

Padding stage disabled entirely, even for explicit camelot2 templates

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `D3_pad_never_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 17 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[spec-value-wins-over-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[unpadded-lowercase-key-agrees-with-head]`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_render[fitted-stem-passes-verbatim]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::TestRender::test_render[stem-is-the-fallback-title]`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::test_a_second_template_produces_a_different_correct_tree_with_no_code_change`
  - `tests/test_naming.py::test_an_optional_field_widens_render_and_parse_together`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if False:

```

### `u39-author-full.E1_budget_ordering_dropped`

Existing guard sample: the budget narrower than written refusal is disabled

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `E1_budget_ordering_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming.py::test_an_invalid_template_is_refused[measuring-narrower-than-writing]`

Old text:

```
        if KEY_PADS.index(self.budget_key_pad) < KEY_PADS.index(self.key_pad):

```

New text:

```
        if False:

```

### `u39-author-full.E2_wheel_bound_widened`

Existing guard sample: the Camelot number bound admits 13 through 19

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `E2_wheel_bound_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 10 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_off_wheel_key_is_rejected_rather_than_normalized[13A]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[bare]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[default]`
  - `tests/test_naming.py::TestSplitAndPadHead::test_split[refuses-unwritable-head]`
  - `tests/test_naming.py::TestTheDeletedDuplicate::test_it_accepted_off_wheel_and_lowercase_keys[off-wheel-13]`
  - `tests/test_naming.py::TestTrailingHead::test_strip_trailing_head[same-wheel-bound]`
  - `tests/test_naming.py::test_is_camelot_agrees_with_parse_camelot`
  - `tests/test_naming.py::test_pad_camelot_normalizes_and_refuses`
  - `tests/test_naming.py::test_parse_and_strip_head[13 is off the wheel]`
  - `tests/test_naming.py::test_parse_camelot[13A]`

Old text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-2])"

```

New text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-9])"

```

### `u39-author-full.M1_refusal_reworded`

Reword the unwritable key refusal, do not append to it

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `M1_refusal_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[bare]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[default]`

Old text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine cannot "

```

New text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine declines to "

```

### `u39-naming-independent.D2_pad_condition_inverted`

Invert the padding condition: pad exactly the off-wheel values and leave real Camelot codes alone

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `D2_pad_condition_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 19 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[spec-value-wins-over-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[unpadded-lowercase-key-agrees-with-head]`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[bare]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[default]`
  - `tests/test_naming.py::TestRender::test_render[fitted-stem-passes-verbatim]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::TestRender::test_render[stem-is-the-fallback-title]`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is None:

```

### `u39-naming-independent.D3_pad_condition_unreachable`

The padding stage never fires for any key_pad value, including camelot2

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `D3_pad_condition_unreachable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 17 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[spec-value-wins-over-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[unpadded-lowercase-key-agrees-with-head]`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_render[fitted-stem-passes-verbatim]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::TestRender::test_render[stem-is-the-fallback-title]`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::test_a_second_template_produces_a_different_correct_tree_with_no_code_change`
  - `tests/test_naming.py::test_an_optional_field_widens_render_and_parse_together`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        if key_pad == "camelot2" and parse_camelot(rendered) is not None:

```

New text:

```
        if key_pad == "impossible-sentinel":

```

### `u39-naming-independent.D4_fake_pad_no_zero_fill`

Padding uppercases but does not zero-fill, a plausible-looking near miss

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `D4_fake_pad_no_zero_fill`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 17 (killed)
- Killed:
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[disagreeing-title-head-leaves-stem-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[key-only-spec-keeps-the-whole-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[no-fields-takes-both-from-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[spec-value-wins-over-the-head]`
  - `tests/test_naming.py::TestAStrippedHeadIsKept::test_the_head_is_kept[unpadded-lowercase-key-agrees-with-head]`
  - `tests/test_naming.py::TestBudgetInteraction::test_build_fits_and_its_result_is_already_in_the_padded_form`
  - `tests/test_naming.py::TestBudgetInteraction::test_the_marker_is_paid_for_in_the_budget_head`
  - `tests/test_naming.py::TestMarkerCoupling::test_the_marker_text_is_a_parameter`
  - `tests/test_naming.py::TestRender::test_render[fitted-stem-passes-verbatim]`
  - `tests/test_naming.py::TestRender::test_render[lossless-carries-no-marker]`
  - `tests/test_naming.py::TestRender::test_render[lossy-marks-right-after-the-head]`
  - `tests/test_naming.py::TestRender::test_render[stem-is-the-fallback-title]`
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::test_a_second_template_produces_a_different_correct_tree_with_no_code_change`
  - `tests/test_naming.py::test_an_optional_field_widens_render_and_parse_together`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            rendered = pad_camelot(rendered)

```

New text:

```
            rendered = rendered.upper()

```

### `u39-naming-independent.E1_budget_ordering_inverted`

Existing guard sample: the budget-narrower-than-written refusal is inverted rather than disabled outright

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `E1_budget_ordering_inverted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_the_key_is_written_and_measured_in_the_same_padded_form`
  - `tests/test_naming.py::test_an_invalid_template_is_refused[measuring-narrower-than-writing]`

Old text:

```
        if KEY_PADS.index(self.budget_key_pad) < KEY_PADS.index(self.key_pad):

```

New text:

```
        if KEY_PADS.index(self.budget_key_pad) > KEY_PADS.index(self.key_pad):

```

### `u39-naming-independent.M1_refusal_reworded`

Reword the unwritable-key refusal instead of appending to it, so an `in` assertion cannot see the change

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `M1_refusal_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[bare]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[default]`

Old text:

```
            f"{name}={value!r} renders as {rendered!r}, which this engine cannot "

```

New text:

```
            f"{name}={value!r} is not something this template can round trip: "

```

### `u41-author-full.D1_dedupe_disabled`

dedupe_stem stops dropping a trailing segment that repeats the lead; an existing guard this unit switched on for real input

- File: `src/cratekit/core/naming.py`
- Source: `u41-author-full.json`, row `D1_dedupe_disabled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 9 (killed)
- Killed:
  - `tests/test_naming.py::TestBudgetInteraction::test_dedupe_runs_before_the_fit_and_the_hash_uses_the_original`
  - `tests/test_naming_apply_cli.py::test_a_collision_answers_with_the_files_that_stayed_put`
  - `tests/test_naming_apply_cli.py::test_a_target_a_collider_holds_is_held_back_too`
  - `tests/test_naming_apply_cli.py::test_a_target_another_mover_still_holds_is_promised_and_then_reported`
  - `tests/test_naming_apply_cli.py::test_an_applied_rename_lands_its_name_and_title_tag_and_converges[a-deduping-rename-converges-on-one-pass]`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-trailing-repeat-of-the-lead-is-deduped]`
  - `tests/test_naming_apply_cli.py::test_the_remediation_only_names_a_hand_rename_over_a_real_collision`
  - `tests/test_naming_apply_cli.py::test_two_files_rendering_to_one_name_are_not_promised_two_renames`
  - `tests/test_naming_apply_cli.py::test_two_targets_differing_only_in_case_are_one_name`

Old text:

```
    deduped = dedupe_stem(spec.stem, spec.title, spec.album, sep=template.segment_sep)

```

New text:

```
    deduped = spec.stem

```

### `u41-author-full.D2_dedupe_structural_rule_widened`

The structural dedupe rule drops its exact trailing match, so an unrelated trailing segment is mutilated

- File: `src/cratekit/core/naming.py`
- Source: `u41-author-full.json`, row `D2_dedupe_structural_rule_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 8 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_file_the_pass_must_leave_proposes_no_rename[13A-is-no-head]`
  - `tests/test_naming_apply_cli.py::test_a_rename_never_replaces_the_body_with_the_title_tag`
  - `tests/test_naming_apply_cli.py::test_both_library_grammars_survive_a_rename`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-segment-only-starting-with-the-lead-survives]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[identity-on-near-match-album]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[identity-when-segments-differ]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[separator-in-title-deduped-via-tags]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[separator-in-title-is-ambiguous-structurally]`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead:

```

### `u41-naming-independent.D3_endswith_widened_to_containment`

The repeat test becomes containment rather than a trailing match, so a lead appearing mid name triggers a cut

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `D3_endswith_widened_to_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 4 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-segment-only-starting-with-the-lead-survives]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[identity-on-near-match-album]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[separator-in-title-deduped-via-tags]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[separator-in-title-is-ambiguous-structurally]`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead and (sep + lead) in stem:

```

### `u41-naming-independent.D6_repeat_widened_to_prefix`

AMBIGUITY MEANS IDENTITY is inverted: a trailing segment that merely BEGINS with the lead counts as a repeat

- File: `src/cratekit/core/naming.py`
- Source: `u41-naming-independent.json`, row `D6_repeat_widened_to_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_apply_cli.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1585 against a baseline of 1585
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[a-segment-only-starting-with-the-lead-survives]`
  - `tests/test_naming_budget.py::TestDedupeStem::test_dedupe_stem[identity-on-near-match-album]`

Old text:

```
        if lead and stem.endswith(sep + lead):

```

New text:

```
        if lead and parts[-1].startswith(lead):

```

