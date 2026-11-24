# Mutation table: u333-replay-before-2x

Measured by `scripts/mutate.py` on 2026-11-24 11:27 UTC, branch `HEAD` at `3b26fad9`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 331.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 09:26 UTC for commit `3b26fad93e24`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 61, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 118 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u328.S2_two_parts_assembled_out_of_order` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u40-author-full.R6_row_still_cut` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1028 | 1 | killed |
| `u42-author-round-2.R2_handler_lookup_imports` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 1020 | 1 | killed |
| `r773-b.R1_doctor_check_not_declared` | `src/cratekit/cli/registry_later.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `u27-adopt-apply-author.R1_marker_restored` | `src/cratekit/cli/registry_modules.py` | user | 1 file(s) | 1017 | collection error | collect-error |
| `u27-reports-round-1.R1_delete_review_precondition` | `src/cratekit/cli/registry_modules.py` | user | 1 file(s) | 417 | 2 | killed |
| `u28-skills-independent.R1_planned_in_restored` | `src/cratekit/cli/registry_modules.py` | user | 1 file(s) | 1016 | collection error | collect-error |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry_modules.py` | maintainer | 2 file(s) | 1024 | collection error | collect-error |
| `u44-author.D1_registry_drops_long_running` | `src/cratekit/cli/registry_modules.py` | maintainer | 1 file(s) | 1019 | collection error | collect-error |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry_modules.py` | user | 3 file(s) | 1108 | collection error | collect-error |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry_modules.py` | user | 2 file(s) | 1436 | collection error | collect-error |
| `r185-r246-author.D2_cloud_gate_restored` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 1020 | 1 | killed |
| `r770-d.C8_native_gate_answered_inline` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 33 | 6 | killed |
| `u263.D22_restamp_declares` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 417 | 1 | killed |
| `u39-author-full.W2_unreachable_gate_restored` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u40-author-full.R3_ungated` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u40-author-full.R5_row_unclaimed` | `src/cratekit/cli/registry_pipeline.py` | user | 2 file(s) | 1028 | 5 | killed |
| `u42-author.R1_planned_marker_returns` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 1017 | collection error | collect-error |
| `u69-b.M20_registry_schema` | `src/cratekit/cli/registry_pipeline.py` | user | 1 file(s) | 40 | 24 | killed |
| `u27-restore-cli-independent.I_H1_the_landed_verb_keeps_its_marker` | `src/cratekit/cli/registry_state.py` | maintainer | 1 file(s) | 1017 | collection error | collect-error |
| `r424.A1_writes_narrowed` | `src/cratekit/cli/registry_sync.py` | user | 1 file(s) | 1020 | 1 | killed |
| `r424.A2_cloud_gate_absent` | `src/cratekit/cli/registry_sync.py` | user | 1 file(s) | 1020 | 1 | killed |
| `r1334.S12_render_no_stale_header` | `src/cratekit/cli/render.py` | user | 1 file(s) | 13 | 2 | killed |
| `r1334.S13_render_header_reworded` | `src/cratekit/cli/render.py` | user | 1 file(s) | 13 | 2 | killed |
| `r1334.S14_render_stale_offers_inline` | `src/cratekit/cli/render.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1334.S15_render_open_gate_drops_inline` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1033 | 3 | killed |
| `r1334.S16_is_gate_screen_no_stale` | `src/cratekit/cli/render.py` | user | 1 file(s) | 13 | 2 | killed |
| `r1334.S17_is_gate_screen_any_stale` | `src/cratekit/cli/render.py` | user | 1 file(s) | 13 | 1 | killed |
| `r1334.S19_screen_test_drops_options_clause` | `src/cratekit/cli/render.py` | user | 1 file(s) | 13 | 1 | killed |
| `r395.M11_render_literal` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1033 | 2 | killed |
| `r678-a.A12_retired_file_unnamed` | `src/cratekit/cli/render.py` | user | 1 file(s) | 34 | 1 | killed |
| `r678-a.A2_drop_the_import_proof_case` | `src/cratekit/cli/render.py` | user | 1 file(s) | 34 | 2 | killed |
| `u27-round-8-independent.E7_readonly_sentence_is_permission` | `src/cratekit/cli/render.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u49-author.V1_the_terminal_screen_stops_showing_it` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1351 | 3 | killed |
| `u97-a.A1_bare_verb_returns` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1437 | 2 | killed |
| `u97-a.A2_rejected_session_says_log_in_again` | `src/cratekit/cli/render.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u97-a.A3_procedure_drops_the_erase` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1437 | 3 | killed |
| `u97-a.A4_procedure_drops_the_flag` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1437 | 3 | killed |
| `u97-a.A5_procedure_drops_the_document` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1437 | 3 | killed |
| `u97-a.A6_remedy_text_drops_the_advice` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1437 | 8 | killed |
| `u97-b.B2_check_table_prints_no_fix` | `src/cratekit/cli/render.py` | user | 1 file(s) | 417 | 2 | killed |
| `u97-c.C2_remediation_line_drops_the_token_branch` | `src/cratekit/cli/render.py` | user | 1 file(s) | 1020 | 3 | killed |
| `r790-d.V1_group_page_refusal` | `src/cratekit/cli/review.py` | user | 1 file(s) | 39 | 2 | killed |
| `r118-b.C1_wizard_probe_escapes` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r118-b.C3_wizard_probe_note_is_advisory` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r345.B1_flags_recorded` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 6 | killed |
| `r345.B2_module_off` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 3 | killed |
| `r345.B3_recorded_kept` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r345.B4_offer_not_demand` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 7 | killed |
| `r345.B5_remote_into_document` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 3 | killed |
| `r345.B6_unknown_module_filter` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 1 | killed |
| `r662-a.M6_flag_not_recorded` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-a.M8_known_spelled_remote_replaced` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-a.M9_replaced_toward_unknown_remote` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 1 | killed |
| `r662-b.M10_composite_with_M9` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M11_replacement_silent` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M12_replacement_not_written` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M13_fix_line_back_to_setup` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M14_token_dropped_beside_others` | `src/cratekit/cli/setup.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `r662-b.M15_advice_names_spelled_remote` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M16_flag_not_declared` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 14 | killed |
| `r662-b.M18_repair_never_runs` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M7_composite_with_M9` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 3 | killed |
| `r83.P3_empty_secret_note_status` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r83.P4_empty_secret_branch` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u27-round-8-independent.S1_act_always_generic` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-round-8-independent.S2_template_write_no_error` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-round-8-independent.S3_unreachable_root_hardcoded` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u283.S15_nothing_entered_fails` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 1 | killed |
| `u283.S1_loop_offers_discogs_again` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u181.S2_gate_never_asked` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u954.M4_sync_stop_exception` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 41 | 1 | killed |
| `u954.M6_auto_step_condition_sync_stop` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 41 | 1 | killed |
| `u168.C7_continue_without_run` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u186.R1_decide_abort` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R2_decide_no_digest` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R3_decide_any_gate` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R4_decide_any_option` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R5_decide_any_digest` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R6_decide_unwired` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 3 | killed |
| `u186.R7_continue_dedupe` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R8_continue_drops_repeat` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u331.S15_foreign_reexport_keeps_every_row` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 67 | 1 | killed |
| `r118-c.B1_slug_is_a_defect` | `src/cratekit/core/cause.py` | user | 1 file(s) | 253 | 2 | killed |
| `r1313.N4_not_found_status_moved` | `src/cratekit/core/cause.py` | user | 1 file(s) | 60 | 3 | killed |
| `r1313.N5_any_status_is_not_found` | `src/cratekit/core/cause.py` | user | 1 file(s) | 60 | 6 | killed |
| `r1349.R8_exit_code` | `src/cratekit/core/cause.py` | user | 1 file(s) | 13 | 2 | killed |
| `r290-author.R3_the_owner_drops_the_type` | `src/cratekit/core/cause.py` | user | 1 file(s) | 126 | 10 | killed |
| `u126.M7_exit_code` | `src/cratekit/core/cause.py` | user | 1 file(s) | 44 | 1 | killed |
| `u27-r80-write-probe-replacement.W1_permission_branch` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-r80-write-probe-replacement.W2_immutable_branch` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-r80-write-probe-replacement.W4_order_access_first` | `src/cratekit/core/cause.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-r80-write-probe-replacement.W7_swallow_guard` | `src/cratekit/core/cause.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `u27-r80-write-probe-replacement.W8_read_probe_flags` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u27-r80-write-probe-zero-rows-repinned.W11_route_path_attribute` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-r80-write-probe-zero-rows-repinned.W3_read_only_branch` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-r80-write-probe-zero-rows-repinned.W5_read_delegation` | `src/cratekit/core/cause.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u27-round-8-independent.C1_immutable_valueerror` | `src/cratekit/core/cause.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-round-8-independent.C2_probe_valueerror` | `src/cratekit/core/cause.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-round-8-independent.C8_two_path_precondition` | `src/cratekit/core/cause.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r1917.V_r926_G1_first` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 12 | killed |
| `r301.F1_section_not_built` | `src/cratekit/core/config.py` | user | 1 file(s) | 253 | 3 | killed |
| `r345.A9_derive_on_load` | `src/cratekit/core/config.py` | user | 1 file(s) | 253 | 9 | killed |
| `r44-a.C4_identity_not_read` | `src/cratekit/core/config.py` | user | 2 file(s) | 584 | 2 | killed |
| `r790-c.C2_config_built` | `src/cratekit/core/config.py` | user | 1 file(s) | 39 | 1 | killed |
| `r926.G10_no_temporary_allowance` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `r926.G11_mkdir_before_check` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 3 | killed |
| `r926.G12_message_drops_path` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 5 | killed |
| `r926.G2_checks_the_shipped_tool` | `src/cratekit/core/config.py` | user | 2 file(s) | 43 | 2 | killed |
| `r926.G3_document_check_dropped` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 4 | killed |
| `r926.G4_document_gets_temporary` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 4 | killed |
| `r926.G5_atomic_write_unchecked` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 2 | killed |
| `r926.G6_lock_unchecked` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `r926.G7_no_root_allows_all` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 6 | killed |
| `r926.G8_target_unresolved` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `r926.G9_temporary_unresolved` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u206.M25_lock_skipped` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 60 | 1 | killed |
| `u254.C1_append_unsynced` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u254.C2_append_one_write` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u254.C3_append_test_root` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 17 | 2 | killed |
| `u254.C4_append_not_append` | `src/cratekit/core/config.py` | user | 1 file(s) | 17 | 1 | killed |
| `u272.C1_no_flush` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 14 (promoted) | killed |
| `u272.C2_full_flush_error_swallowed` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u272.C3_full_flush_then_sync` | `src/cratekit/core/config.py` | maintainer | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u272.C4_full_flush_never_asked` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 5 (promoted) | killed |
| `u272.C5_eio_counts_as_unsupported` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u272.C6_no_plain_sync` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 12 (promoted) | killed |
| `u272.C7_error_names_no_path` | `src/cratekit/core/config.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u299.U13_from_dict_applies_overrides` | `src/cratekit/core/config.py` | user | 1 file(s) | 253 | 4 | killed |
| `u329.R1_config_remedy_drifts_from_the_canonical_text` | `src/cratekit/core/config.py` | user | 2 file(s) | 1046 | 4 | killed |
| `r301.V4_label_shape_loose` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 4 | killed |
| `r345.A1_colon_required` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 1 | killed |
| `r345.A2_single_letter` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 6 | killed |
| `r345.A3_name_shape` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 6 | killed |
| `r345.A4_leading_hyphen` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 3 | killed |
| `r345.A5_trailing_space` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 3 | killed |
| `r44-a.C3_identity_not_written` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 1 | killed |
| `r662-a.M2_spelled_path_compared_whole` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 2 | killed |
| `r662-b.M1b_several_remotes_compared` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 417 | 1 | killed |
| `r662-b.M3b_blank_remote_disagrees` | `src/cratekit/core/config_schema.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `u197-m6.M6_composite` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 1 | killed |
| `u197.M2_retired_mapping_empty` | `src/cratekit/core/config_schema.py` | user | 2 file(s) | 670 | 3 | killed |
| `u233.C1_schema_default_moves` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 19 | 1 | killed |
| `u233.C2_schema_gains_a_key` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 19 | 1 | killed |
| `u299.U12_pin_refusal_remedy` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 1 | killed |
| `u331.S04_membership_ignores_explicit_toggles` | `src/cratekit/core/config_schema.py` | user | 1 file(s) | 253 | 1 | killed |
| `r227.V1_validator_not_called` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 6 | killed |
| `r227.V2_no_ceiling` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 1 | killed |
| `r227.V3_bool_is_a_day_count` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 1 | killed |
| `r301.V1_validator_not_called` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 17 | killed |
| `r301.V2_any_domain` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 4 | killed |
| `r301.V3_suffix_without_dot` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 2 | killed |
| `r301.V6_bool_is_a_bound` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 1 | killed |
| `r301.V7_zero_is_a_bound` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 1 | killed |
| `r345.A10_spelled_remote_wins` | `src/cratekit/core/config_validate.py` | user | 2 file(s) | 670 | 9 | killed |
| `r345.A6_one_remote` | `src/cratekit/core/config_validate.py` | user | 2 file(s) | 670 | 2 | killed |
| `r345.A8_validate_wiring` | `src/cratekit/core/config_validate.py` | user | 2 file(s) | 670 | 30 | killed |
| `r44-a.C1_rule_identity_may_be_a_path` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 3 | killed |
| `r44-a.C2_blank_identity_is_absence` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 253 | 2 | killed |
| `r662-a.M4_validator_drops_disagreement` | `src/cratekit/core/config_validate.py` | user | 2 file(s) | 670 | 7 | killed |
| `r662-a.M5_validator_message_loses_flag` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 417 | 1 | killed |
| `r744.C1_equal_bounds_accepted` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 65 | 1 | killed |
| `r744.C2_bool_accepted` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 65 | 1 | killed |
| `r790-c.C1_config_floor` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 39 | 1 | killed |
| `u117-operator.D13_config_validation` | `src/cratekit/core/config_validate.py` | maintainer | 1 file(s) | 24 | 1 | killed |
| `u157.F1_cut_zero` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 41 | 2 | killed |
| `u157.F2_cut_nan` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 41 | 1 | killed |
| `u197.M1_config_fold` | `src/cratekit/core/config_validate.py` | user | 2 file(s) | 670 | 2 | killed |
| `u206.M22_days_validation_dropped` | `src/cratekit/core/config_validate.py` | user | 1 file(s) | 60 | 1 | killed |
| `u241.M09_ceiling_ignores_the_reserve` | `src/cratekit/core/cores.py` | user | 1 file(s) | 42 | 7 | killed |
| `u93-recursive-analysis.D10_sorted_items` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D11_absolute_id` | `src/cratekit/core/discovery.py` | maintainer | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D12_parent_id` | `src/cratekit/core/discovery.py` | maintainer | 1 file(s) | 33 | 2 | killed |
| `u93-recursive-analysis.D13_singular` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 2 | killed |
| `u93-recursive-analysis.D15_unreadable_empty` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 6 | killed |
| `u93-recursive-analysis.D16_none_filter` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 9 | killed |
| `u93-recursive-analysis.D17_and_more` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D18_strings_shape` | `src/cratekit/core/discovery.py` | maintainer | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D19_resume_half` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D1_dotfile` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D20_frozen_links` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D2_is_file` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D3_suffix` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D4_default_mode` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 2 | killed |
| `u93-recursive-analysis.D5_dot_directory` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D6_link_declined` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 4 | killed |
| `u93-recursive-analysis.D7_prune_in_place` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 33 | 1 | killed |
| `u93-recursive-analysis.D9_onerror` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u329.R2_run_setup_token_text` | `src/cratekit/core/exit_codes.py` | user | 1 file(s) | 26 | 1 | killed |
| `u185.F11_difference_memberships` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F12_difference_appeared` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F1_root_must_be_a_folder` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 4 | killed |
| `u185.F2_root_must_be_at_the_top` | `src/cratekit/core/foreign_tree.py` | user | 2 file(s) | 98 | 4 | killed |
| `u185.F3_descendants_walked` | `src/cratekit/core/foreign_tree.py` | user | 3 file(s) | 144 | 9 | killed |
| `u185.F4_create_inside` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F5_second_root` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F7_modify_inside` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F8_moved_in` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `u185.F9_membership` | `src/cratekit/core/foreign_tree.py` | user | 1 file(s) | 31 | 1 | killed |
| `r289-b.D1_no_chunking` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `r289-b.D3_unknown_name_gets_a_state` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `r290-author.J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 44 | killed |
| `r290-author.J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 43 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 62 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 21 | killed |
| `r290-author.J5_causeless_block_returns` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 1 | killed |
| `r290-author.J6_causeless_block_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 1 | killed |
| `r290-author.J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 21 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 126 | 33 | killed |
| `r390-a.A1_retry_re_arms_unconditionally` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 0 | 0 | error |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `r390-a.A3_a_failed_job_with_no_cause_is_refused` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-a.A4_refusal_drops_the_permanent_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-a.A5_refusal_drops_the_inner_cause` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `r390-b.B6_envelope_drops_the_reasons` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `u140.B3_refreeze_any_state` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.B4_refreeze_writes_nothing_new` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 29 | 7 | killed |
| `u235.S1_enqueue_ignores_a_given_job_id` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 26 | killed |
| `u270.J1_claim_batch_size_floor` | `src/cratekit/core/jobs.py` | maintainer | 1 file(s) | 20 | 1 | killed |
| `u270.J2_claim_batch_order` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 20 | 8 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 4 file(s) | 183 | 45 | killed |
| `u301.J1_job_row_answers_none` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 2 | killed |
| `u301.J2_release_claims_any_driver` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 84 | 1 | killed |
| `r380.G3_retryable_requires_every_item` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `r380.G5_permanent_failures_still_offer_resume` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 4 | killed |
| `r390-b.B1_last_reason_restored` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-b.B2_reasons_in_reverse_order` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-b.B3_message_does_not_name_the_reasons` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-b.B4_detail_drops_permanent_reasons` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `r390-b.B5_one_shared_reason_is_also_mixed` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 3 | killed |
| `r390-b.B7_drive_passes_no_reasons_to_the_envelope` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `r704-a.E2_job_verdict_needs_every_item_retryable` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `u169.E1_declined_accepts_retryable` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 2 | killed |
| `u169.E2_drive_fails_a_decline` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 4 | killed |
| `u169.E3_decline_writes_failed` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 3 | killed |
| `u169.E4_decline_drops_cause` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `u169.E6_failed_cause_hides_declines` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 84 | 1 | killed |
| `u270.J3_park_releases_the_batch` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 3 | killed |
| `u270.J4_signal_releases_the_batch` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 1 | killed |
| `u270.J5_declined_outcome` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 1 | killed |
| `u270.J6_missing_outcome_fails` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 1 | killed |
| `u270.J7_raise_is_every_outcome` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 2 | killed |
| `u270.J8_stop_is_the_signal` | `src/cratekit/core/jobs_drive.py` | user | 1 file(s) | 20 | 1 | killed |
| `u270.J9_outcome_type_check` | `src/cratekit/core/jobs_drive.py` | maintainer | 1 file(s) | 20 | 1 | killed |
| `r83-round-2.I1_fold_case` | `src/cratekit/core/preflight.py` | user | 1 file(s) | 417 | 1 | killed |
| `r83-round-2.I3_configured_compare_exact` | `src/cratekit/core/preflight.py` | user | 1 file(s) | 417 | 1 | killed |
| `u27-round-8-independent.E4_path_missing_reads_ok` | `src/cratekit/core/preflight.py` | user | 1 file(s) | 417 | 2 | killed |
| `u27-round-8-independent.E5_unmounted_reads_foreign` | `src/cratekit/core/preflight.py` | user | 1 file(s) | 417 | 2 | killed |
| `u27-round-8-independent.E6_write_table_shares_read` | `src/cratekit/core/preflight.py` | user | 1 file(s) | 417 | 3 | killed |
| `u329.P1_rb_changes_wrong_family` | `src/cratekit/core/rb_changes.py` | user | 1 file(s) | 44 | 18 | killed |
| `r1665.W1_check_opens_the_capture` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 25 | 12 | killed |
| `u329.P2_rb_copies_wrong_family` | `src/cratekit/core/rb_copies.py` | user | 1 file(s) | 25 | 20 | killed |
| `r1890.P5_gate_name_in_rb_nodes` | `src/cratekit/core/rb_nodes.py` | maintainer | 1 file(s) | 1020 | 1 | killed |
| `r235-b.M22_nested_namesake_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 2 | killed |
| `r235-b.M23_playlist_is_a_root` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 40 | 1 | killed |
| `u111-a.A1_folder_refused` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-a.A3_parent_not_folder` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-a.A4_memberships_unmarked` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-a.A5_node_unmarked` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-a.A7_content_compared` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-b.A10_renumber_scoped` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-b.A12_removed_keeps_no_live` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 2 | killed |
| `u111-b.A13_confinement_raises` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 1 | killed |
| `u111-b.A8_membership_owner` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 2 | killed |
| `u111-b.A9_planned_move_made` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 4 | killed |
| `u127.W1_writable_always` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 16 | 1 | killed |
| `u127.W2_writable_reason_drift` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 16 | 1 | killed |
| `u329.P3_rb_nodes_wrong_family` | `src/cratekit/core/rb_nodes.py` | user | 1 file(s) | 30 | 17 | killed |
| `u953.M11_is_folder_any_attribute` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 73 | 4 | killed |
| `r923.N19_default_is_an_analysis_column` | `src/cratekit/core/rb_tables.py` | user | 3 file(s) | 93 | 31 | killed |
| `u111-a.A6_playlist_not_removable` | `src/cratekit/core/rb_tables.py` | user | 1 file(s) | 30 | 3 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 331 | 8 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 331 | 8 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 331 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 331 | 8 | killed |
| `r746-a.G4_read_back_walks_session_new_only` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 44 | 1 | killed |
| `r746-a.G6_analysis_tables_not_checked` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 44 | 1 | killed |
| `r746-a.G7_sql_value_check_disarmed` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r746-d.G5_content_row_read_back_against_five_not_ten` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u185.G1_commit_guard_called` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 13 | killed |
| `u185.G2_unread_refuses` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G3_pending_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 7 | killed |
| `u185.G4_second_reading_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G5_reading_at_open` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 12 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 463 | 158 | killed |
| `r1890.P9_sidecar_suffix_typed_in_restore_perform` | `src/cratekit/core/restore_perform.py` | user | 1 file(s) | 253 | 1 | killed |
| `r815-a.W4_the_next_ordinal_is_past_the_floor` | `src/cratekit/core/review.py` | user | 1 file(s) | 76 | 2 | killed |
| `r815-a.W6_redescribe_only_an_open_item` | `src/cratekit/core/review.py` | user | 1 file(s) | 76 | 2 | killed |
| `r840-c.C1_the_function_is_handed_the_payload_as_it_stands` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 34 | killed |
| `r840-c.C2_the_function_is_only_handed_an_open_item` | `src/cratekit/core/review.py` | user | 1 file(s) | 61 | 4 | killed |
| `r790-d.R1_grouping_kinds` | `src/cratekit/core/review_groups.py` | user | 1 file(s) | 39 | 1 | killed |
| `r790-d.R2_label_beyond` | `src/cratekit/core/review_groups.py` | user | 1 file(s) | 39 | 7 | killed |
| `r798-c.H2_only_a_hold_in_force_is_dropped` | `src/cratekit/core/review_holds.py` | user | 1 file(s) | 138 | 1 | killed |
| `r815-a.W1_withhold_only_an_open_item` | `src/cratekit/core/review_holds.py` | user | 1 file(s) | 76 | 5 | killed |
| `r815-a.W2_a_returned_hold_is_not_withheld` | `src/cratekit/core/review_holds.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-a.W3_the_floor_is_never_lowered` | `src/cratekit/core/review_holds.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-a.W5_a_refresh_keeps_the_withheld_word` | `src/cratekit/core/review_holds.py` | user | 1 file(s) | 76 | 1 | killed |
| `r650-a.A1_tier_five_sets_nothing` | `src/cratekit/core/routing.py` | user | 1 file(s) | 67 | 3 | killed |
| `r650-a.A2_tier_five_flags_everything` | `src/cratekit/core/routing.py` | user | 1 file(s) | 50 | 1 | killed |
| `r650-a.A6_declared_literal_rule_flagged` | `src/cratekit/core/routing.py` | user | 1 file(s) | 67 | 1 | killed |
| `r798-a.K1_the_first_rule_that_matches_wins` | `src/cratekit/core/routing.py` | user | 1 file(s) | 138 | 3 | killed |
| `r798-a.K2_one_word_of_the_labels_kind_passes` | `src/cratekit/core/routing.py` | user | 1 file(s) | 138 | 3 | killed |
| `r798-a.K3_a_hold_needs_a_known_word` | `src/cratekit/core/routing.py` | user | 1 file(s) | 138 | 1 | killed |
| `r798-a.K4_a_label_of_any_kind_passes` | `src/cratekit/core/routing.py` | user | 1 file(s) | 138 | 3 | killed |
| `r798-a.K5_a_kind_nothing_names_is_not_judged` | `src/cratekit/core/routing.py` | user | 1 file(s) | 138 | 1 | killed |
| `r798-d.K11_the_shared_matcher_reads_a_substring_needle` | `src/cratekit/core/routing.py` | user | 1 file(s) | 138 | 58 | killed |
| `u155.R1_exact_match` | `src/cratekit/core/routing.py` | user | 1 file(s) | 48 | 2 | killed |
| `u155.R2_tagger_branch` | `src/cratekit/core/routing.py` | user | 1 file(s) | 48 | 4 | killed |
| `u155.R3_tagger_spelling` | `src/cratekit/core/routing.py` | user | 1 file(s) | 48 | 1 | killed |
| `r118-a.A10_forget_uses_the_record_sentence` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r118-a.A11_record_sentence_reworded` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r118-a.A12_env_override_no_longer_short_circuits` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r118-a.A1_blanket_returns_empty` | `src/cratekit/core/secrets.py` | user | 2 file(s) | 670 | 11 | killed |
| `r118-a.A2_enoent_refuses_too` | `src/cratekit/core/secrets.py` | user | 2 file(s) | 670 | 34 | killed |
| `r118-a.A3_unparseable_returns_empty` | `src/cratekit/core/secrets.py` | user | 2 file(s) | 670 | 2 | killed |
| `r118-a.A4_wrong_shape_returns_empty` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r118-a.A5_refusal_drops_the_path` | `src/cratekit/core/secrets.py` | user | 2 file(s) | 670 | 4 | killed |
| `r118-a.A6_refusal_not_raised_from` | `src/cratekit/core/secrets.py` | user | 2 file(s) | 670 | 3 | killed |
| `r118-a.A8_damaged_reports_as_unreadable` | `src/cratekit/core/secrets.py` | maintainer | 1 file(s) | 253 | 1 | killed |
| `r118-a.A9_record_uses_the_read_sentence` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r118-b.D1_index_written_before_the_read_back` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r118-b.D2_keychain_removed_before_the_index` | `src/cratekit/core/secrets.py` | user | 2 file(s) | 670 | 6 | killed |
| `r118-c.A7_unreadable_remedy_is_set_credential` | `src/cratekit/core/secrets.py` | user | 1 file(s) | 253 | 1 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 2 file(s) | 444 | 3 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 3 file(s) | 467 | 24 | killed |
| `r1255.S7_log_unlisted_predicate` | `src/cratekit/core/session.py` | user | 1 file(s) | 27 | 1 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 1 file(s) | 34 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 1 file(s) | 34 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 2 file(s) | 60 | 5 | killed |
| `r501-a.S4_excusal_state` | `src/cratekit/core/session.py` | user | 1 file(s) | 34 | 1 | killed |
| `r598-a.A5_holder_never_recorded` | `src/cratekit/core/session.py` | user | 1 file(s) | 417 | 1 | killed |
| `u331.S05_room_reexport_checks_nothing` | `src/cratekit/core/session.py` | user | 1 file(s) | 25 | 1 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session_ack.py` | user | 1 file(s) | 417 | 1 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session_ack.py` | user | 1 file(s) | 417 | 3 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session_ack.py` | user | 1 file(s) | 1020 | 1 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session_ack.py` | user | 1 file(s) | 417 | 1 | killed |
| `u329.P6_session_ack_wrong_family` | `src/cratekit/core/session_ack.py` | user | 1 file(s) | 82 | 28 | killed |
| `u329.A2_session_accessor_returns_the_writer` | `src/cratekit/core/session_call_time.py` | user | 1 file(s) | 331 | 96 | killed |
| `r598-a.A3_liveness_not_consulted` | `src/cratekit/core/session_holders.py` | user | 1 file(s) | 417 | 1 | killed |
| `u329.P7_session_holders_wrong_family` | `src/cratekit/core/session_holders.py` | user | 1 file(s) | 417 | 1 | killed |
| `r44-a.S2_proved_widened` | `src/cratekit/core/session_volumes.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-a.S4_inside_root_unheld` | `src/cratekit/core/session_volumes.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-a.S5_not_destructive` | `src/cratekit/core/session_volumes.py` | user | 1 file(s) | 331 | 1 | killed |
| `r44-a.S7_probe_the_target` | `src/cratekit/core/session_volumes.py` | user | 1 file(s) | 331 | 2 | killed |
| `u329.P8_session_volumes_wrong_family` | `src/cratekit/core/session_volumes.py` | user | 1 file(s) | 331 | 7 | killed |
| `r1677.C1_no_measure` | `src/cratekit/core/snapshot.py` | user | 1 file(s) | 25 | 1 | killed |
| `r1677.C3_store_not_passed` | `src/cratekit/core/snapshot.py` | user | 1 file(s) | 25 | 1 | killed |
| `r1677.N1_every_failure_is_room` | `src/cratekit/core/snapshot.py` | user | 1 file(s) | 25 | 1 | killed |
| `r432-b.B5_lock_on_the_library_volume` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 27 | 11 | killed |
| `r432-b.B6_lock_directory_renamed` | `src/cratekit/core/state_files.py` | maintainer | 1 file(s) | 23216 | 1 (promoted) | killed |
| `u278.M1_gate_follows_state` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 60 | 1 | killed |
| `u299.U1_installation_never_restored` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 253 | 3 | killed |
| `u299.U2_installation_area_passed` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 417 | 3 | killed |
| `u299.U3_installation_medium_passed` | `src/cratekit/core/state_files.py` | maintainer | 1 file(s) | 253 | 5 | killed |
| `u299.U4_library_root` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 253 | 17 | killed |
| `u299.U5_library_snapshot_passed` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 253 | 6 | killed |
| `u299.U7_library_extras_passed` | `src/cratekit/core/state_files.py` | user | 1 file(s) | 253 | 4 | killed |
| `r798-a.K6_the_default_kind_is_one_a_rule_names` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 138 | 1 | killed |
| `r798-a.K7_a_needle_is_folded_when_loaded` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 138 | 1 | killed |
| `r798-a.K8_a_kind_is_one_word` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 138 | 1 | killed |
| `u111-d.F1_old_differs_from_intake` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 30 | 2 | killed |
| `u155.T10_source_claimed` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 1 | killed |
| `u155.T11_shape_check` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 3 | killed |
| `u155.T12_sources_type` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 2 | killed |
| `u155.T13_live_places` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 2 | killed |
| `u155.T14_tagging_index` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 4 | killed |
| `u155.T1_version_guard` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 4 | killed |
| `u155.T2_band_guard` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 2 | killed |
| `u155.T3_id_pattern` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 1 | killed |
| `u155.T4_empty_display` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 1 | killed |
| `u155.T5_duplicate_id` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 1 | killed |
| `u155.T6_id_collision` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 4 | killed |
| `u155.T7_display_collision` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 5 | killed |
| `u155.T8_empty_sources` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 4 | killed |
| `u155.T9_source_alias` | `src/cratekit/core/taxonomy_build.py` | user | 1 file(s) | 48 | 2 | killed |

## Zero rows and what they owe

- `u27-round-8-independent.E7_readonly_sentence_is_permission` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.S1_act_always_generic` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.S2_template_write_no_error` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.S3_unreachable_root_hardcoded` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-r80-write-probe-replacement.W1_permission_branch` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-r80-write-probe-replacement.W2_immutable_branch` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-r80-write-probe-replacement.W4_order_access_first` (maintainer facing): maintainer facing, composite not required
- `u27-r80-write-probe-zero-rows-repinned.W11_route_path_attribute` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-r80-write-probe-zero-rows-repinned.W3_read_only_branch` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-r80-write-probe-zero-rows-repinned.W5_read_delegation` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.C8_two_path_precondition` (maintainer facing): maintainer facing, composite not required
- `r926.G9_temporary_unresolved` (maintainer facing): maintainer facing, composite not required
- `u93-recursive-analysis.D9_onerror` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-a.G7_sql_value_check_disarmed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r746-d.G5_content_row_read_back_against_five_not_ten` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u328.S2_two_parts_assembled_out_of_order`

ENTRIES: assemble the sync part before the pipeline part, so the table's order, which help follows, changes

- File: `src/cratekit/cli/registry.py`
- Source: `u328.json`, row `S2_two_parts_assembled_out_of_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_table_is_every_part_in_order_and_each_file_is_under_the_bar`

Old text:

```
    *PIPELINE_VERBS,
    *SYNC_VERBS,

```

New text:

```
    *SYNC_VERBS,
    *PIPELINE_VERBS,

```

### `u40-author-full.R6_row_still_cut`

Leave row 18 dispositioned Cut while a verb claims it, which is the coupling across two trees

- File: `src/cratekit/cli/registry.py`
- Source: `u40-author-full.json`, row `R6_row_still_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1028 against a baseline of 1028
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
- Collected: 1020 against a baseline of 1020
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

### `r773-b.R1_doctor_check_not_declared`

registry: the verb no longer declares library.paths_resolved

- File: `src/cratekit/cli/registry_later.py`
- Source: `r773-b.json`, row `R1_doctor_check_not_declared`
- Moved: the same text, now in src/cratekit/cli/registry_later.py, was in src/cratekit/cli/registry.py
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

### `u27-adopt-apply-author.R1_marker_restored`

Put planned_in back on the entry, so the conformance suite stops driving the landed verb

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u27-adopt-apply-author.json`, row `R1_marker_restored`
- Moved: U328 moved adopt.move's entry to the modules part, which does not import ADOPT_APPLY_CLI_UNIT, so the row as written ended in a NameError and broke collection for another reason; the same marker is put back on the same entry, by the constant's value, U27
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1017 against a baseline of 1020
- Kills: 2 (collect-error)
- Note: collection changed: 1017 collected against a baseline of 1020. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
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
        planned_in="U27",
    ),
    # ── Deletion: one surface, two modules
```

### `u27-reports-round-1.R1_delete_review_precondition`

Stop delete.review declaring the Trash check as a precondition

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u27-reports-round-1.json`, row `R1_delete_review_precondition`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
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

### `u28-skills-independent.R1_planned_in_restored`

the skills.install registry entry gets planned_in back, so the conformance properties skip it again

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u28-skills-independent.json`, row `R1_planned_in_restored`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1016 against a baseline of 1020
- Kills: 1 (collect-error)
- Note: collection changed: 1016 collected against a baseline of 1020. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1024 against a baseline of 1028
- Kills: 3 (collect-error)
- Note: collection changed: 1024 collected against a baseline of 1028. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`

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

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u44-author.json`, row `D1_registry_drops_long_running`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1019 against a baseline of 1020
- Kills: 1 (collect-error)
- Note: collection changed: 1019 collected against a baseline of 1020. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`

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

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u45-round-1.json`, row `V3_marker_restored`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_jobs.py`
- Collected: 1108 against a baseline of 1112
- Kills: 4 (collect-error)
- Note: collection changed: 1108 collected against a baseline of 1112. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`
  - `tests/test_jobs.py::test_a_job_queued_for_a_verb_that_has_not_landed_refuses_rather_than_importing`

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

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u45-round-1.json`, row `V5_module_toggle_dropped`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1436 against a baseline of 1437
- Kills: 4 (collect-error)
- Note: collection changed: 1436 collected against a baseline of 1437. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
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

### `r185-r246-author.D2_cloud_gate_restored`

Declare the cloud sync decision on a verb that opens no database, the half the contract suite calls spurious

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `r185-r246-author.json`, row `D2_cloud_gate_restored`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

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

### `r770-d.C8_native_gate_answered_inline`

registry: declare intake.file.native as an ordinary gate, answerable on the run that found it

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `r770-d.json`, row `C8_native_gate_answered_inline`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
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

### `u263.D22_restamp_declares`

registry: analyze restamp no longer declares binary.ffmpeg

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u263.json`, row `D22_restamp_declares`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
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

### `u39-author-full.W2_unreachable_gate_restored`

name.apply redeclares the cloud sync decision its work can never raise

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u39-author-full.json`, row `W2_unreachable_gate_restored`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
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

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u40-author-full.json`, row `R3_ungated`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
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

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u40-author-full.json`, row `R5_row_unclaimed`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`
- Collected: 1028 against a baseline of 1028
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

### `u42-author.R1_planned_marker_returns`

Restore planned_in on acquire.download, which is the state that hid rows 6 and 7

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u42-author.json`, row `R1_planned_marker_returns`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1017 against a baseline of 1020
- Kills: 1 (collect-error)
- Note: collection changed: 1017 collected against a baseline of 1020. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
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

### `u69-b.M20_registry_schema`

Declare the verb plan/1 in the registry, which the human renderer does not show

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u69-b.json`, row `M20_registry_schema`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
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

### `u27-restore-cli-independent.I_H1_the_landed_verb_keeps_its_marker`

Put planned_in back on restore.list, which is what would disarm the conformance properties again

- File: `src/cratekit/cli/registry_state.py`
- Source: `u27-restore-cli-independent.json`, row `I_H1_the_landed_verb_keeps_its_marker`
- Moved: the same text, now in src/cratekit/cli/registry_state.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1017 against a baseline of 1020
- Kills: 1 (collect-error)
- Note: collection changed: 1017 collected against a baseline of 1020. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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

### `r424.A1_writes_narrowed`

Restore the four local write surfaces the verb never reaches

- File: `src/cratekit/cli/registry_sync.py`
- Source: `r424.json`, row `A1_writes_narrowed`
- Moved: the same text, now in src/cratekit/cli/registry_sync.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

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
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_every_verb_that_writes_the_database_declares_the_cloud_sync_decision`

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

### `r1334.S12_render_no_stale_header`

render_gate: no line saying the plan moved and that an answer now is taken over it

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S12_render_no_stale_header`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
    lines = [STALE_SCREEN, ""] if stale else []
```

New text:

```
    lines = []
```

### `r1334.S13_render_header_reworded`

STALE_SCREEN: reworded, never appended

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S13_render_header_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
    "The plan moved since this gate was answered. This is the plan this run "
```

New text:

```
    "This gate's plan has changed since it was answered. This is the plan this run "
```

### `r1334.S14_render_stale_offers_inline`

render_gate: a stale screen offers the inline -d answer, which is compared with the moved one and refused

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S14_render_stale_offers_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`

Old text:

```
        if not stale:
            lines.append(f"  or:      rerun with -d {gate}=<option>")
```

New text:

```
        lines.append(f"  or:      rerun with -d {gate}=<option>")
```

### `r1334.S15_render_open_gate_drops_inline`

render_gate: the open gate's inline line dropped too, the stale test inverted

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S15_render_open_gate_drops_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_gate_stale_screen.py`
- Collected: 1033 against a baseline of 1033
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_human_mode_renders_what_the_verb_showed_and_is_unchanged_without_it`
  - `tests/test_gate_stale_screen.py::test_the_open_gates_screen_is_unchanged`
  - `tests/test_gate_stale_screen.py::test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes`

Old text:

```
        if not stale:
            lines.append(f"  or:      rerun with -d {gate}=<option>")
```

New text:

```
        if stale:
            lines.append(f"  or:      rerun with -d {gate}=<option>")
```

### `r1334.S16_is_gate_screen_no_stale`

is_gate_screen: a stale never prints its screen, the human sees two digests only

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S16_is_gate_screen_no_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
    return cause.reason == "decision-stale" and "options" in (cause.detail or {})
```

New text:

```
    return False
```

### `r1334.S17_is_gate_screen_any_stale`

is_gate_screen: every stale prints a gate screen, a verb's own write handle stale with no options included

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S17_is_gate_screen_any_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`

Old text:

```
    return cause.reason == "decision-stale" and "options" in (cause.detail or {})
```

New text:

```
    return cause.reason == "decision-stale"
```

### `r1334.S19_screen_test_drops_options_clause`

is_gate_screen: drop the options clause in the round one fix's form, so a verb's own stale prints the header over no plan

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S19_screen_test_drops_options_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`
- Collected: 13 against a baseline of 13
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`

Old text:

```
    return cause.reason == "decision-stale" and "options" in (cause.detail or {})
```

New text:

```
    return cause.reason == "decision-stale" and "gate" in (cause.detail or {})
```

### `r395.M11_render_literal`

Put the old bare pip literal back in the parser stub

- File: `src/cratekit/cli/render.py`
- Source: `r395.json`, row `M11_render_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_install_command.py`
- Collected: 1033 against a baseline of 1033
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command`
  - `tests/test_install_command.py::test_the_parser_stub_and_the_workers_read_one_source`

Old text:

```
    return extras.install_command(entry.extras)
```

New text:

```
    return f"pip install '{registry.DISTRIBUTION}[{entry.extras}]'"
```

### `r678-a.A12_retired_file_unnamed`

the retired intake file's name is dropped from the proof line

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A12_retired_file_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`

Old text:

```
    filed = f"intake file retired to {PurePath(str(retired)).name}" if retired else None
```

New text:

```
    filed = None
```

### `r678-a.A2_drop_the_import_proof_case`

the original defect for intake imported: render never asks for the proof

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A2_drop_the_import_proof_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`

Old text:

```
    lines += render_import_proof(envelope)

```

New text:

```
(empty)
```

### `u27-round-8-independent.E7_readonly_sentence_is_permission`

Give a read only volume the permission-grant sentence, the defect round 8 closed one layer up

- File: `src/cratekit/cli/render.py`
- Source: `u27-round-8-independent.json`, row `E7_readonly_sentence_is_permission`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        cause_module.AccessKind.READ_ONLY: (
            "The volume holding it is mounted read only, so it refuses every writer on "
            "this machine and no permission grant can change that. Remount it read write, "
            "release the medium's write protection, or write somewhere else"
        ),
```

New text:

```
        cause_module.AccessKind.READ_ONLY: (
            "The operating system refused this account, which is a permission to grant "
            "rather than a defect in this program. Grant this interpreter access to the "
            "path, or choose one it can already reach"
        ),
```

### `u49-author.V1_the_terminal_screen_stops_showing_it`

Remove the shown branch from render_gate, so the carried facts reach JSON and never reach a person

- File: `src/cratekit/cli/render.py`
- Source: `u49-author.json`, row `V1_the_terminal_screen_stops_showing_it`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`
- Collected: 1351 against a baseline of 1351
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_human_mode_renders_what_the_verb_showed_and_is_unchanged_without_it`
  - `tests/test_cli_contract.py::test_the_profile_gate_shows_the_delta_the_digest_was_taken_over`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`

Old text:

```
    shown = detail.get("shown")
    if isinstance(shown, Mapping) and shown:
        lines.append("")
        lines += _shown_lines(shown)
```

New text:

```
(empty)
```

### `u97-a.A1_bare_verb_returns`

_COMMANDS: offer the bare crate login again, the exact defect R-411 measured, which shadows the advice entirely

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A1_bare_verb_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1437 against a baseline of 1437
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`

Old text:

```
    Remedy.AUTHENTICATE_PROVIDER: None,
```

New text:

```
    Remedy.AUTHENTICATE_PROVIDER: "crate login",
```

### `u97-a.A2_rejected_session_says_log_in_again`

_ADVICE: put REAUTHENTICATE_PROVIDER back to log in again, the same instruction nothing performs on the likelier path

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A2_rejected_session_says_log_in_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`

Old text:

```
        "the provider rejected the stored session and crate login cannot mint another, it "
        "only records one; " + _PROVIDER_SESSION_PROCEDURE
```

New text:

```
        "the provider rejected the stored credential; log in again"
```

### `u97-a.A3_procedure_drops_the_erase`

_PROVIDER_SESSION_PROCEDURE: name mint and record and not the erase, which is what leaves a plaintext token on disk

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A3_procedure_drops_the_erase`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1437 against a baseline of 1437
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`

Old text:

```
    "crate login provider-session --from-file, then erase the plaintext file, which "
    "docs/adapters.md in the project's repository sets out step by step"
```

New text:

```
    "crate login provider-session --from-file, which "
    "docs/adapters.md in the project's repository sets out step by step"
```

### `u97-a.A4_procedure_drops_the_flag`

_PROVIDER_SESSION_PROCEDURE: name the subcommand without --from-file, so the person is told to run a verb that refuses with no source

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A4_procedure_drops_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1437 against a baseline of 1437
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`

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
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1437 against a baseline of 1437
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`

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
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1437 against a baseline of 1437
- Kills: 8 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`
  - `tests/test_doctor.py::test_a_module_enabled_without_its_credential_is_reported_with_the_fix`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_grant_path_access_advice_claims_neither_act_over_the_other`
  - `tests/test_doctor.py::test_the_human_rendering_shows_the_checks_rather_than_only_a_status`

Old text:

```
    return _COMMANDS.get(remedy) or _ADVICE.get(remedy)
```

New text:

```
    return _COMMANDS.get(remedy)
```

### `u97-b.B2_check_table_prints_no_fix`

render_checks: print the check row and swallow its fix line, so the human report names every failure and no remedy

- File: `src/cratekit/cli/render.py`
- Source: `u97-b.json`, row `B2_check_table_prints_no_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_missing_provider_session_is_offered_the_procedure_and_not_the_bare_verb`
  - `tests/test_doctor.py::test_the_human_rendering_shows_the_checks_rather_than_only_a_status`

Old text:

```
        if words:
            lines.append(f"         fix: {words}")
```

New text:

```
        if False:
            lines.append(f"         fix: {words}")
```

### `u97-c.C2_remediation_line_drops_the_token_branch`

composite for B5: drop the remedy branch altogether, so every cause with a token falls to its first step or the exit code's generic summary. Shows what the renderer holds when the precedence between the two holds nothing

- File: `src/cratekit/cli/render.py`
- Source: `u97-c.json`, row `C2_remediation_line_drops_the_token_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[authenticate-provider-  fix: crate login]`
  - `tests/test_cli_contract.py::test_a_provider_session_remedy_names_three_acts_and_not_a_login_nothing_performs[reauthenticate-provider-  fix: the provider rejected the stored credential; log in again]`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`

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

### `r790-d.V1_group_page_refusal`

_list_grouped: accept --after and --limit and ignore them

- File: `src/cratekit/cli/review.py`
- Source: `r790-d.json`, row `V1_group_page_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 39 against a baseline of 39
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_page_limit_with_a_grouping_refuses_rather_than_being_ignored`
  - `tests/test_label_offer_window.py::test_grouping_needs_a_queue_and_has_no_pages`

Old text:

```
    if not ctx.args.queue or ctx.args.after is not None or ctx.args.limit is not None:
```

New text:

```
    if not ctx.args.queue:
```

### `r118-b.C1_wizard_probe_escapes`

The presence probe raises out of the wizard, discarding the whole report over a configuration already saved

- File: `src/cratekit/cli/setup.py`
- Source: `r118-b.json`, row `C1_wizard_probe_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
            try:
                already = secrets.exists(str(name))
            except CratekitError as exc:
```

New text:

```
            try:
                already = secrets.exists(str(name))
            except ArithmeticError as exc:
```

### `r118-b.C3_wizard_probe_note_is_advisory`

An unanswerable presence question is reported as INFO, so setup exits clean over a question it could not answer

- File: `src/cratekit/cli/setup.py`
- Source: `r118-b.json`, row `C3_wizard_probe_note_is_advisory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
                    doctor.Status.FAIL,
                    f"whether {name} is recorded could not be answered, {cause.message}",
```

New text:

```
                    doctor.Status.INFO,
                    f"whether {name} is recorded could not be answered, {cause.message}",
```

### `r345.B1_flags_recorded`

_resolve_backup: never record a flag, so --backup-dest is accepted and written nowhere

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B1_flags_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[flag]`
  - `tests/test_doctor.py::test_a_declined_offer_still_records_the_flags_that_were_given`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_backup_flags_are_recorded_even_when_the_module_is_off`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`

Old text:

```
        if flag:
            _put(document, key, wizard.resolve(key, flag=flag, question=""))
```

New text:

```
        if False:
            _put(document, key, wizard.resolve(key, flag=flag, question=""))
```

### `r345.B2_module_off`

_resolve_backup: offer the destinations whatever the profile says, so slim is asked about a module it does not have

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B2_module_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_backup_flags_are_recorded_even_when_the_module_is_off`
  - `tests/test_doctor.py::test_the_wizard_asks_nothing_about_backup_when_the_module_is_off`

Old text:

```
    if "backup" not in membership.modules:
```

New text:

```
    if False:
```

### `r345.B3_recorded_kept`

_resolve_backup: treat every destination as missing, so a re-run asks for values already recorded

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B3_recorded_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_declined_offer_still_records_the_flags_that_were_given`
  - `tests/test_doctor.py::test_the_wizard_keeps_recorded_backup_destinations_without_asking`

Old text:

```
    missing = [key for key in config.BACKUP_DESTINATION_KEYS if not recorded(key)]
```

New text:

```
    missing = list(config.BACKUP_DESTINATION_KEYS)
```

### `r345.B4_offer_not_demand`

_resolve_backup: skip the offer and ask outright, so a silent full profile run refuses

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B4_offer_not_demand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 7 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[prompt]`
  - `tests/test_doctor.py::test_a_declined_offer_still_records_the_flags_that_were_given`
  - `tests/test_doctor.py::test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_asks_for_the_backup_destinations_when_the_module_is_on`
  - `tests/test_doctor.py::test_the_wizard_records_nothing_for_backup_when_the_offer_goes_unanswered`

Old text:

```
    elif missing and not wizard.optional(
```

New text:

```
    elif False and not wizard.optional(
```

### `r345.B5_remote_into_document`

_resolve_backup: do not write the derived remote into the document, so the file carries no remote

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B5_remote_into_document`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_declined_offer_still_records_the_flags_that_were_given`
  - `tests/test_doctor.py::test_backup_flags_are_recorded_even_when_the_module_is_off`
  - `tests/test_doctor.py::test_the_wizard_asks_for_the_backup_destinations_when_the_module_is_on`

Old text:

```
    if derived is not None:
        _put(document, "backup.remote", derived)
```

New text:

```
    if False:
        _put(document, "backup.remote", derived)
```

### `r345.B6_unknown_module_filter`

_resolve_backup: hand the raw modules table to profiles.resolve, so a mistyped module raises before validate

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B6_unknown_module_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback`

Old text:

```
        {k: bool(v) for k, v in modules.items() if k in profiles.MODULES}
```

New text:

```
        {k: bool(v) for k, v in modules.items()}
```

### `r662-a.M6_flag_not_recorded`

the --backup-remote flag is parsed and never written into the document

- File: `src/cratekit/cli/setup.py`
- Source: `r662-a.json`, row `M6_flag_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_backup_remote_flag_replaces_a_spelled_remote_rclone_knows`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`

Old text:

```
    if args.backup_remote:
        _put(
```

New text:

```
    if False:
        _put(
```

### `r662-a.M8_known_spelled_remote_replaced`

a spelled remote rclone knows is replaced anyway, which is R-345's rule broken

- File: `src/cratekit/cli/setup.py`
- Source: `r662-a.json`, row `M8_known_spelled_remote_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-it]`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`

Old text:

```
    if remotes is None or spelled.split(":", 1)[0] in remotes or expected not in remotes:
```

New text:

```
    if remotes is None or expected not in remotes:
```

### `r662-a.M9_replaced_toward_unknown_remote`

the replacement no longer requires rclone to know the destinations' remote, so an empty dump swaps a right name for a typo

- File: `src/cratekit/cli/setup.py`
- Source: `r662-a.json`, row `M9_replaced_toward_unknown_remote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`

Old text:

```
    if remotes is None or spelled.split(":", 1)[0] in remotes or expected not in remotes:
```

New text:

```
    if remotes is None or spelled.split(":", 1)[0] in remotes:
```

### `r662-b.M10_composite_with_M9`

M10 and M9 together, what the absent binary guard holds once the known destination guard is gone

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M10_composite_with_M9`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-absent]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`

Old text:

```
    remotes = machine.rclone_remotes(rclone) if rclone is not None else None
    if remotes is None or spelled.split(":", 1)[0] in remotes or expected not in remotes:
```

New text:

```
    remotes = machine.rclone_remotes(rclone)
    if remotes is None or spelled.split(":", 1)[0] in remotes:
```

### `r662-b.M11_replacement_silent`

the replacement is made and no note says so

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M11_replacement_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_spelled_remote_rclone_lacks_is_replaced_by_the_destinations_remote`

Old text:

```
    _put(document, "backup.remote", expected)
    wizard.note(
        "setup.backup.remote",
        "backup remote",
        doctor.Status.INFO,
        (
            f"backup.remote was {spelled!r}, which rclone has no remote by, and "
            f"every backup destination names {expected!r}, so it was replaced "
            f"with {expected!r}"
        ),
    )
```

New text:

```
    _put(document, "backup.remote", expected)
```

### `r662-b.M12_replacement_not_written`

the note is made and the document keeps the spelled remote

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M12_replacement_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_spelled_remote_rclone_lacks_is_replaced_by_the_destinations_remote`

Old text:

```
    _put(document, "backup.remote", expected)
    wizard.note(
```

New text:

```
    wizard.note(
```

### `r662-b.M13_fix_line_back_to_setup`

the refusal's remediation reverts to the run-setup token for every problem, the pre R-662 fix line

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M13_fix_line_back_to_setup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem`

Old text:

```
    disagreement = config.backup_remote_disagreement(document)
    if disagreement is None:
        return Remediation(remedy=Remedy.RUN_SETUP, steps=tuple(problems))
```

New text:

```
    disagreement = config.backup_remote_disagreement(document)
    if True:
        return Remediation(remedy=Remedy.RUN_SETUP, steps=tuple(problems))
```

### `r662-b.M14_token_dropped_beside_others`

the token is dropped whenever the disagreement is present, even beside other problems

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M14_token_dropped_beside_others`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem`

Old text:

```
    if len(problems) > 1:
        return Remediation(remedy=Remedy.RUN_SETUP, steps=steps)
```

New text:

```
    if len(problems) > 2:
        return Remediation(remedy=Remedy.RUN_SETUP, steps=steps)
```

### `r662-b.M15_advice_names_spelled_remote`

the flag step recommends the spelled name, the one already refused, instead of the destinations' name

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M15_advice_names_spelled_remote`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem`

Old text:

```
        f"re-run crate setup with --backup-remote {expected} to record the remote "
```

New text:

```
        f"re-run crate setup with --backup-remote {spelled} to record the remote "
```

### `r662-b.M16_flag_not_declared`

the parser no longer declares --backup-remote

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M16_flag_not_declared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 14 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[flag]`
  - `tests/test_doctor.py::test_a_bare_folder_name_is_refused_by_the_wizard_however_it_arrives[prompt]`
  - `tests/test_doctor.py::test_a_mistyped_module_name_is_still_a_named_problem_not_a_traceback`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_an_install_with_no_templates_offers_no_closed_set_rather_than_an_empty_one`
  - `tests/test_doctor.py::test_setup_leaves_under_the_code_a_refusing_check_reserved`
  - `tests/test_doctor.py::test_setup_writes_nothing_beside_the_library_until_the_volume_is_asserted`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_doctor.py::test_the_wizard_writes_the_active_template_on_a_linux_style_ordinary_directory`
  - `tests/test_doctor.py::test_the_wizard_writes_the_active_template_once_the_volume_is_the_recorded_one`

Old text:

```
    parser.add_argument(
        "--backup-remote",
        help="the rclone remote the three destinations name, replacing a recorded one",
    )
```

New text:

```
(empty)
```

### `r662-b.M18_repair_never_runs`

the rclone repair is never called

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M18_repair_never_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_spelled_remote_rclone_lacks_is_replaced_by_the_destinations_remote`

Old text:

```
    if not args.backup_remote:
        _replace_a_remote_rclone_lacks(wizard, document, machine)
```

New text:

```
    if False:
        _replace_a_remote_rclone_lacks(wizard, document, machine)
```

### `r662-b.M7_composite_with_M9`

M7 and M9 together, what the unreadable configuration guard holds once the known destination guard is gone; batch a's M7 is the row it pairs with

- File: `src/cratekit/cli/setup.py`
- Source: `r662-b.json`, row `M7_composite_with_M9`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-absent]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-unreadable]`

Old text:

```
    if remotes is None or spelled.split(":", 1)[0] in remotes or expected not in remotes:
```

New text:

```
    remotes = remotes or {}
    if spelled.split(":", 1)[0] in remotes:
```

### `r83.P3_empty_secret_note_status`

R-347: the wizard's empty credential note is FAIL instead of INFO

- File: `src/cratekit/cli/setup.py`
- Source: `r83.json`, row `P3_empty_secret_note_status`
- Moved: U303 shortened the comment above the note to its rule; the INFO status of the empty credential note, the guard this row flips, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
```

New text:

```
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
```

### `r83.P4_empty_secret_branch`

R-347: remove the NothingEntered branch so the unreadable branch catches it

- File: `src/cratekit/cli/setup.py`
- Source: `r83.json`, row `P4_empty_secret_branch`
- Moved: U303 shortened the comment inside the branch to one line; the NothingEntered branch, the guard this row removes, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_credential_offer_accepted_and_left_empty_is_the_same_note_as_a_no`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
            except prompt.NothingEntered:
                # Accepted then left empty is the same as a no (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
                    f"{name} is not recorded and was not entered; doctor reports it",
                )
                continue

```

New text:

```
(empty)
```

### `u27-round-8-independent.S1_act_always_generic`

_act stops asking render.access_note and always closes with the generic clause

- File: `src/cratekit/cli/setup.py`
- Source: `u27-round-8-independent.json`, row `S1_act_always_generic`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    note = render.access_note(exc)
    return f" {note}" if note is not None else f" {otherwise}"
```

New text:

```
    return f" {otherwise}"
```

### `u27-round-8-independent.S2_template_write_no_error`

The wizard's template WRITE site stops handing its exception to the finding

- File: `src/cratekit/cli/setup.py`
- Source: `u27-round-8-independent.json`, row `S2_template_write_no_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            + _act(exc, "Choose a library root this account can already write"),
            Remedy.GRANT_PATH_ACCESS,
            error=exc,
```

New text:

```
            + _act(exc, "Choose a library root this account can already write"),
            Remedy.GRANT_PATH_ACCESS,
```

### `u27-round-8-independent.S3_unreachable_root_hardcoded`

Put the hard coded Full Disk Access advice back into _unreachable_root

- File: `src/cratekit/cli/setup.py`
- Source: `u27-round-8-independent.json`, row `S3_unreachable_root_hardcoded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        f"defect and it is not a missing drive."
    ) + _act(exc, "Choose a library root this account can already reach")
```

New text:

```
        f"defect and it is not a missing drive. Grant this interpreter access "
        f"to the path, or choose a library root it can already reach"
    )
```

### `u283.S15_nothing_entered_fails`

_link_discogs: an empty entry is a FAIL rather than the skip note

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S15_nothing_entered_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`

Old text:

```
            wizard.note(key, title, doctor.Status.INFO, f"nothing was entered; {unlinked}")
```

New text:

```
            wizard.note(key, title, doctor.Status.FAIL, f"nothing was entered; {unlinked}")
```

### `u283.S1_loop_offers_discogs_again`

_capture_credentials: drop the pass over the Discogs check, so the bare loop offers and stores the token unchecked beside the step

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S1_loop_offers_discogs_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_wizard_offers_every_credential_the_profile_needs_and_records_it`
  - `tests/test_doctor.py::test_the_wizard_reports_no_check_key_twice`

Old text:

```
        if key == DISCOGS_CHECK:
            continue
```

New text:

```
        if False:
            continue
```

### `u181.S2_gate_never_asked`

sync land _vocals: never stop at the gate, so a pass lands rows with no score unasked

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S2_gate_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.land]`

Old text:

```
    unable = tail.vocals_unavailable()
    if unable is None:
```

New text:

```
    unable = tail.vocals_unavailable()
    if True:
```

### `u954.M4_sync_stop_exception`

REKORDBOX_STEPS: the sync stop claims the next launch reads Normal even when every row carries the tag

- File: `src/cratekit/cli/tail.py`
- Source: `u954.json`, row `M4_sync_stop_exception`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_the_sync_stop_runs_dynamic_first_and_normal_last`

Old text:

```
    f"{drift.NORMAL_SETTINGS}, so the mode the next launch reads is Normal unless "
    f"every row carries the tag; {AUTO_ANALYSIS_STEP}",
```

New text:

```
    f"{drift.NORMAL_SETTINGS}, so the mode the next launch reads is Normal even if "
    f"every row carries the tag; {AUTO_ANALYSIS_STEP}",
```

### `u954.M6_auto_step_condition_sync_stop`

AUTO_ANALYSIS_STEP in tail: the sync stop's copy tells the closing Normal run whatever the rows

- File: `src/cratekit/cli/tail.py`
- Source: `u954.json`, row `M6_auto_step_condition_sync_stop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    f"{drift.DYNAMIC_SETTINGS}, and then, when they did and a row lacks the tag, one "
```

New text:

```
    f"{drift.DYNAMIC_SETTINGS}, and then, whatever the rows carry, always one "
```

### `u168.C7_continue_without_run`

_continued: dispatch the verb again without --run, as a new run

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C7_continue_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`

Old text:

```
    envelope = cli.dispatch(["--run", state.run_id, *state.argv], stderr=sys.stderr)
```

New text:

```
    envelope = cli.dispatch([*state.argv], stderr=sys.stderr)
```

### `u186.R1_decide_abort`

same_plan_answered: drop the abort refusal, so two aborts over one plan warn

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R1_decide_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_both_answers_are_abort`

Old text:

```
    if option == gates.RETIRE_OPTION or offered is None:
```

New text:

```
    if offered is None:
```

### `u186.R2_decide_no_digest`

same_plan_answered: drop the no digest refusal, so a run offered nothing matches a sibling that recorded none

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R2_decide_no_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_this_run_was_offered_no_digest`

Old text:

```
    if option == gates.RETIRE_OPTION or offered is None:
```

New text:

```
    if option == gates.RETIRE_OPTION:
```

### `u186.R3_decide_any_gate`

same_plan_answered: match an answer on any gate, not the one being answered

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R3_decide_any_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_answered_another_gate`

Old text:

```
            name == gate and held.option == option and held.digest == offered
```

New text:

```
            held.option == option and held.digest == offered
```

### `u186.R4_decide_any_option`

same_plan_answered: match an answer of any option, so a sibling's abort warns over an apply

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R4_decide_any_option`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_aborted`

Old text:

```
            name == gate and held.option == option and held.digest == offered
```

New text:

```
            name == gate and held.digest == offered
```

### `u186.R5_decide_any_digest`

same_plan_answered: match an answer over any digest, so another plan's approval warns

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R5_decide_any_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_answered_another_plan`

Old text:

```
            name == gate and held.option == option and held.digest == offered
```

New text:

```
            name == gate and held.option == option
```

### `u186.R6_decide_unwired`

decide: never compute the repeat, so run decide says nothing over a sibling that approved the same plan

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R6_decide_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`

Old text:

```
    said = same_plan_answered(state, spec.name, ctx.args.option)
```

New text:

```
    said = []
```

### `u186.R7_continue_dedupe`

_continued: drop the dedupe, so a sibling named by decide and by the stale gate is said twice

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R7_continue_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_continue_says_a_sibling_once_when_the_verb_stops_at_its_gate_again`

Old text:

```
    repeated = [one for one in said if one not in envelope.warnings]
```

New text:

```
    repeated = list(said)
```

### `u186.R8_continue_drops_repeat`

_continued: drop the repeat on a continued run's envelope

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R8_continue_drops_repeat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`

Old text:

```
    repeated = [one for one in said if one not in envelope.warnings]
```

New text:

```
    repeated = []
```

### `u331.S15_foreign_reexport_keeps_every_row`

active_taxonomy.outside_foreign: the re-export the favourites home and the pair discovery call is replaced by one that keeps every row, so a playlist inside another app's folder counts as the Favorites home

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `u331.json`, row `S15_foreign_reexport_keeps_every_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
from cratekit.core.foreign_tree import outside as outside_foreign

```

New text:

```

def outside_foreign(rows, _every):
    return list(rows)


```

### `r118-c.B1_slug_is_a_defect`

credential-index-unreadable maps to INTERNAL, so a sidecar the person can repair is reported as a defect to file

- File: `src/cratekit/core/cause.py`
- Source: `r118-c.json`, row `B1_slug_is_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`

Old text:

```
        "credential-index-unreadable": ExitCode.PRECONDITION,
```

New text:

```
        "credential-index-unreadable": ExitCode.INTERNAL,
```

### `r1313.N4_not_found_status_moved`

NOT_FOUND_STATUS: 410 rather than 404, so no 404 is a not found through the nearest status

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N4_not_found_status_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[404]`

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
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 6 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_failed_lookup_is_never_kept_and_the_next_one_asks[outage]`
  - `tests/test_isrc_cache.py::test_a_failed_lookup_is_never_kept_and_the_next_one_asks[rejected-session]`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[500]`
  - `tests/test_isrc_cache.py::test_the_catalogue_never_keeps_a_failure[outage]`
  - `tests/test_isrc_cache.py::test_the_catalogue_never_keeps_a_failure[rejected-session]`

Old text:

```
    return nearest_status(exc) == NOT_FOUND_STATUS
```

New text:

```
    return nearest_status(exc) is not None
```

### `r1349.R8_exit_code`

cause: gate-not-reached exits as decision required, the code a chain reads as an open gate

- File: `src/cratekit/core/cause.py`
- Source: `r1349.json`, row `R8_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`
- Collected: 13 against a baseline of 13
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_the_refusal_is_not_an_open_gate_to_any_reader`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
        "gate-not-reached": ExitCode.PRECONDITION,
```

New text:

```
        "gate-not-reached": ExitCode.DECISION_REQUIRED,
```

### `r290-author.R3_the_owner_drops_the_type`

Make cause.rebuilt return the plain type for every input, so both hops drop the blocked bit at once with no hand written rebuild for the static guard to find

- File: `src/cratekit/core/cause.py`
- Source: `r290-author.json`, row `R3_the_owner_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 10 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause[JobBlocked]`
  - `tests/test_job_outcome.py::test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause[JobCancelled]`

Old text:

```
            return kind(cause)
```

New text:

```
            return CratekitError(cause)
```

### `u126.M7_exit_code`

Register the refusal as PRECONDITION, a command line fault, not the library's

- File: `src/cratekit/core/cause.py`
- Source: `u126.json`, row `M7_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_approval_at_one_link_is_not_applied_at_another_and_no_majority_refuses`

Old text:

```
        "link-majority-unclear": ExitCode.LIBRARY_PREREQUISITE,
```

New text:

```
        "link-majority-unclear": ExitCode.PRECONDITION,
```

### `u27-r80-write-probe-replacement.W1_permission_branch`

Drop the os.access branch, so a mode or ACL refusal is not attributed

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W1_permission_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)

```

New text:

```
(empty)
```

### `u27-r80-write-probe-replacement.W2_immutable_branch`

Drop the immutable branch, so a Finder Locked file reports permission

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W2_immutable_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)

```

New text:

```
(empty)
```

### `u27-r80-write-probe-replacement.W4_order_access_first`

Ask os.access before ST_RDONLY, so a read only volume reads as a permission

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W4_order_access_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)

```

New text:

```
        if not os.access(path, os.W_OK, effective_ids=effective):
            return AccessRefusal(kind=AccessKind.PERMISSION, path=path)
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)
        if _immutable(path):
            return AccessRefusal(kind=AccessKind.LOCKED, path=path)

```

### `u27-r80-write-probe-replacement.W7_swallow_guard`

Narrow the guard to OSError, dropping the ValueError an unrepresentable path raises

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W7_swallow_guard`
- Moved: the same guard in _probe_writable; its comment was shortened by the prose pass (U299)
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised`

Old text:

```
    except (OSError, ValueError):
        # :func:`_probe_readable`'s two guards, for the same reason.

```

New text:

```
    except OSError:
        # :func:`_probe_readable`'s two guards, for the same reason.

```

### `u27-r80-write-probe-replacement.W8_read_probe_flags`

Make the read probe write capable, the shape the reports allowlist forbids

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W8_read_probe_flags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/modules/test_reports.py::test_the_allowlist_admits_no_writer_this_guard_cannot_name`

Old text:

```
        handle = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
```

New text:

```
        handle = os.open(path, os.O_RDWR | os.O_NONBLOCK)
```

### `u27-r80-write-probe-zero-rows-repinned.W11_route_path_attribute`

Drop the path attribute the connection site attaches, so the driver route classifies nothing

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-zero-rows-repinned.json`, row `W11_route_path_attribute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if name.startswith("SQLITE_CANTOPEN"):
        return _probe_readable(str(path))
    return _probe_writable(str(path))
```

New text:

```
    if name.startswith("SQLITE_CANTOPEN"):
        return _probe_readable(str(path))
    return None
```

### `u27-r80-write-probe-zero-rows-repinned.W3_read_only_branch`

Drop the ST_RDONLY branch, so a read only volume reports permission. Was zero before the pin

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-zero-rows-repinned.json`, row `W3_read_only_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return AccessRefusal(kind=AccessKind.READ_ONLY, path=path)

```

New text:

```
(empty)
```

### `u27-r80-write-probe-zero-rows-repinned.W5_read_delegation`

Drop the read probe delegation, so an unreachable path answers silence. Was zero before the pin

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-zero-rows-repinned.json`, row `W5_read_delegation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    refused = _probe_readable(path)
    if refused is not None:
        return refused

```

New text:

```
(empty)
```

### `u27-round-8-independent.C1_immutable_valueerror`

Drop the ValueError catch in _immutable, so an embedded-null path raises out of the refusal handler

- File: `src/cratekit/core/cause.py`
- Source: `u27-round-8-independent.json`, row `C1_immutable_valueerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised`

Old text:

```
        flags = getattr(os.lstat(path), "st_flags", 0)
    except (OSError, ValueError):
```

New text:

```
        flags = getattr(os.lstat(path), "st_flags", 0)
    except OSError:
```

### `u27-round-8-independent.C2_probe_valueerror`

Drop the ValueError catch in _probe, so an embedded-null path raises out of the refusal handler

- File: `src/cratekit/core/cause.py`
- Source: `u27-round-8-independent.json`, row `C2_probe_valueerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_path_no_filesystem_can_represent_is_answered_rather_than_raised`

Old text:

```
    except OSError as probe:
        return _from_os_error(probe)
    except ValueError:
        return None
```

New text:

```
    except OSError as probe:
        return _from_os_error(probe)
```

### `u27-round-8-independent.C8_two_path_precondition`

Drop the both-paths-present precondition, so a one-path permission error is re-measured

- File: `src/cratekit/core/cause.py`
- Source: `u27-round-8-independent.json`, row `C8_two_path_precondition`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if exc.filename2 is not None and exc.filename is not None:
            path = _refused_of_two(exc, path)
```

New text:

```
        path = _refused_of_two(exc, path)
```

### `r1917.V_r926_G1_first`

The brief's verification, r926.G1_never_checks replayed (first of two in a row on one container): the guard returns at once, so every write the file aims outside lands, and the file must remove it

- File: `src/cratekit/core/config.py`
- Source: `r1917.json`, row `V_r926_G1_first`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 12 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
```

New text:

```
    if True:
        return
    root = _TEST_WRITE_ROOT
```

### `r301.F1_section_not_built`

The recognition section is never read from the file, so every install gets the default

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `F1_section_not_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-host-identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-monthly_calls-250]`
  - `tests/test_config.py::test_the_recognition_defaults_bound_the_month_and_name_one_region`

Old text:

```
        recognition=_build(RecognitionConfig, data.get("recognition") or {}),
```

New text:

```
        recognition=RecognitionConfig(),
```

### `r345.A9_derive_on_load`

from_dict: do not derive backup.remote from the destinations

- File: `src/cratekit/core/config.py`
- Source: `r345.json`, row `A9_derive_on_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_an_rclone_remote_is_accepted`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[full]`
  - `tests/test_config.py::test_an_unset_backup_destination_stays_allowed[slim]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[Sicherung_\xfc]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[b2]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[gdrive-2.old]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[me@gdrive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[my drive]`
  - `tests/test_config.py::test_every_name_rclone_can_store_is_accepted_as_a_remote[work+home]`

Old text:

```
            overrides={"remote": derived_backup_remote(data)},
```

New text:

```
            overrides=None,
```

### `r44-a.C4_identity_not_read`

Never read a rule's identity in, so every configured rule arrives unrecorded

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C4_identity_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_deletion.py`
- Collected: 584 against a baseline of 584
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`
  - `tests/test_deletion.py::test_the_rules_the_pass_builds_from_configuration_carry_each_recorded_identity`

Old text:

```
                    volume_id=entry.get(PREFIX_VOLUME_IDENTITY_KEY),
```

New text:

```
                    volume_id=None,
```

### `r790-c.C2_config_built`

from_dict: ignore the labels section and always take the default

- File: `src/cratekit/core/config.py`
- Source: `r790-c.json`, row `C2_config_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
        labels=_build(LabelsConfig, data.get("labels") or {}),
```

New text:

```
        labels=LabelsConfig(),
```

### `r926.G10_no_temporary_allowance`

The primitives lose the system temporary allowance, the strict rule the review round measured at 101 refusals

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G10_no_temporary_allowance`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root`

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

### `r926.G11_mkdir_before_check`

save creates the configuration directory before the lock is built, so a refused write leaves a directory behind

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G11_mkdir_before_check`
- Moved: Same lines in save; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 3 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_path_outside_the_root_is_refused_with_the_isolation_in_place`
  - `tests/test_config_test_root.py::test_a_path_resolution_that_leaves_the_root_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`

Old text:

```
    with _write_lock(target):
        mkdir_private(target.parent)
        atomic_write_bytes(config.to_toml_bytes(), target)
```

New text:

```
    mkdir_private(target.parent)
    with _write_lock(target):
        atomic_write_bytes(config.to_toml_bytes(), target)
```

### `r926.G12_message_drops_path`

The no root refusal stops naming the path it refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G12_message_drops_path`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 5 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
            f"refused to write {path}: this process is "
            f"running under pytest and no test root is registered, so the "
```

New text:

```
            f"refused to write the file: this process is "
            f"running under pytest and no test root is registered, so the "
```

### `r926.G2_checks_the_shipped_tool`

The guard runs in a process without pytest too, so the shipped tool refuses every configuration save

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G2_checks_the_shipped_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config_update.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_process_without_pytest_loaded_is_never_checked`
  - `tests/test_config_update.py::test_three_real_processes_writing_at_once_all_keep_their_answers`

Old text:

```
    if "pytest" not in sys.modules:
        return
    root = _TEST_WRITE_ROOT
```

New text:

```
    if False:
        return
    root = _TEST_WRITE_ROOT
```

### `r926.G3_document_check_dropped`

_write_lock no longer checks, so the configuration document is held only by the primitives' temporary allowance

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G3_document_check_dropped`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 4 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G4_document_gets_temporary`

The configuration document is given the system temporary allowance the primitives have

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G4_document_gets_temporary`
- Moved: Same lines in _write_lock; U298 renamed _exclusive_lock to the public exclusive_lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 4 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_the_configuration_is_not_allowed_the_system_temporary_folder`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    _refuse_write_outside_test_root(path)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

New text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    return exclusive_lock(path.with_name(path.name + ".migrate.lock"))
```

### `r926.G5_atomic_write_unchecked`

atomic_write_bytes no longer checks, so a ledger or token write from an unisolated test lands anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G5_atomic_write_unchecked`
- Moved: Same lines in atomic_write_bytes; U298 renamed _mkdir_private to the public mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[atomic-write]`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

New text:

```
    mkdir_private(path.parent)
    fd, tmp = tempfile.mkstemp(
```

### `r926.G6_lock_unchecked`

_exclusive_lock no longer checks, so a session lock from an unisolated test is created anywhere

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G6_lock_unchecked`
- Moved: Same lines in the lock's __enter__; U298 renamed the class to exclusive_lock and _mkdir_private to mkdir_private
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`

Old text:

```
        _refuse_write_outside_test_root(self.path, system_temporary=True)
        mkdir_private(self.path.parent)
```

New text:

```
        mkdir_private(self.path.parent)
```

### `r926.G7_no_root_allows_all`

With no root registered the allowed set is the filesystem root, so the R-926 probe writes the live config again

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G7_no_root_allows_all`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 6 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_lock_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[atomic-write]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_migration_write_back_is_refused`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_a_save_is_refused_and_names_the_path`
  - `tests/test_config_test_root.py::test_with_the_isolation_removed_an_update_is_refused_and_writes_nothing`

Old text:

```
    allowed = [] if root is None else [root.resolve()]
```

New text:

```
    allowed = [Path(os.sep)] if root is None else [root.resolve()]
```

### `r926.G8_target_unresolved`

The target is compared as spelled, so a link inside the root aimed outside it passes

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G8_target_unresolved`
- Moved: Same lines in _refuse_write_outside_test_root; U298 renamed _is_inside to the public is_inside
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_link_inside_the_root_aimed_outside_it_is_refused`

Old text:

```
    target = path.resolve()
    if any(is_inside(target, each) for each in allowed):
```

New text:

```
    target = path
    if any(is_inside(target, each) for each in allowed):
```

### `r926.G9_temporary_unresolved`

The system temporary directory is compared as spelled, /var against /private/var on macOS, so every scratch write is refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G9_temporary_unresolved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
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

### `u206.M25_lock_skipped`

Cache._locked: yield as held without taking the lock

- File: `src/cratekit/core/config.py`
- Source: `u206.json`, row `M25_lock_skipped`
- Moved: U298 replaced isrc_cache.Cache._locked's body with config.lock_within, which _locked now returns; the same non blocking flock in the same poll loop, so dropping it yields held without the lock
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`

Old text:

```
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                had = True
```

New text:

```
            try:
                had = True
```

### `u254.C1_append_unsynced`

append_durable_bytes: return without syncing the appended record

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C1_append_unsynced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_every_append_is_synced_before_the_mark_returns`

Old text:

```
            view = view[os.write(fd, view) :]
        os.fsync(fd)
```

New text:

```
            view = view[os.write(fd, view) :]
```

### `u254.C2_append_one_write`

append_durable_bytes: make one write call and drop what it did not take

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C2_append_one_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`

Old text:

```
        while view:
            view = view[os.write(fd, view) :]
```

New text:

```
        if view:
            view = view[os.write(fd, view) :]
```

### `u254.C3_append_test_root`

append_durable_bytes: drop the test root refusal

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C3_append_test_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_state_write_outside_every_temporary_folder_is_refused[durable-append]`
  - `tests/test_config_test_root.py::test_a_state_write_outside_the_root_is_refused_with_the_isolation_in_place[durable-append]`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

### `u254.C4_append_not_append`

append_durable_bytes: open for writing at the start of the file rather than its end

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C4_append_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_an_append_inside_the_root_adds_to_the_file_and_never_creates_one`

Old text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY)
```

### `u272.C1_no_flush`

flush_to_disk: open and close the path and flush nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C1_no_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 14 (killed)
- Promoted: subset killed 0, full suite killed 14
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
    try:
        _flush_descriptor(fd)
    except OSError as exc:
```

New text:

```
    try:
        pass
    except OSError as exc:
```

### `u272.C2_full_flush_error_swallowed`

_flush_descriptor: fall back to the plain sync on every error of the full flush, an I/O error included

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C2_full_flush_error_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`

Old text:

```
            if exc.errno not in _FULL_FLUSH_UNSUPPORTED:
                raise
```

New text:

```
            if False:
                raise
```

### `u272.C3_full_flush_then_sync`

_flush_descriptor: drop the return after a full flush, so the plain sync runs as well

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C3_full_flush_then_sync`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
            _full_flush(fd, _FULL_FLUSH)
            return
```

New text:

```
            _full_flush(fd, _FULL_FLUSH)
```

### `u272.C4_full_flush_never_asked`

_flush_descriptor: never ask for the full flush, the plain sync on every platform

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C4_full_flush_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 5 (killed)
- Promoted: subset killed 0, full suite killed 5
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
    if _FULL_FLUSH is not None:
        try:
```

New text:

```
    if False:
        try:
```

### `u272.C5_eio_counts_as_unsupported`

_FULL_FLUSH_UNSUPPORTED: count an I/O error as a filesystem without the full flush

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C5_eio_counts_as_unsupported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`

Old text:

```
frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY})
```

New text:

```
frozenset({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY, errno.EIO})
```

### `u272.C6_no_plain_sync`

_flush_descriptor: drop the plain sync, so a platform without the full flush flushes nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C6_no_plain_sync`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 12 (killed)
- Promoted: subset killed 0, full suite killed 12
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
                raise
    os.fsync(fd)

```

New text:

```
                raise

```

### `u272.C7_error_names_no_path`

flush_to_disk: raise a flush error as it came, naming no file

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C7_error_names_no_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`

Old text:

```
        if exc.filename is not None:
            raise
        raise OSError(exc.errno, exc.strerror or str(exc), str(path)) from exc
```

New text:

```
        raise
```

### `u299.U13_from_dict_applies_overrides`

config.from_dict: the overrides are left to validation, so the built config keeps the file's root

- File: `src/cratekit/core/config.py`
- Source: `u299.json`, row `U13_from_dict_applies_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_relocated_root_carries_the_database_that_sat_under_it`
  - `tests/test_config.py::test_a_save_under_a_relocation_writes_a_file_that_loads_again`
  - `tests/test_config.py::test_the_backup_destination_check_reads_the_effective_mapping`
  - `tests/test_config.py::test_the_prefix_map_survives_a_remount_because_it_interpolates`

Old text:

```
    data = _apply_env_overrides(data)
    problems = validate(data)
```

New text:

```
    problems = validate(data)
```

### `u329.R1_config_remedy_drifts_from_the_canonical_text`

config.Remedy is a vocabulary of its own again, its run-setup token spelled differently from the canonical one

- File: `src/cratekit/core/config.py`
- Source: `u329.json`, row `R1_config_remedy_drifts_from_the_canonical_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_config_update.py`
- Collected: 1046 against a baseline of 1046
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_an_unconfigured_machine_refuses_with_a_precondition_and_a_remedy`
  - `tests/test_cli_contract.py::test_every_module_declaring_its_own_remedies_stays_inside_one_vocabulary`
  - `tests/test_cli_contract.py::test_every_module_local_remedy_renders_to_something_a_user_can_act_on`
  - `tests/test_config_update.py::test_two_wizards_answering_one_key_differently_refuse_and_write_nothing`

Old text:

```
from cratekit.core.exit_codes import Remedy as Remedy

```

New text:

```
from cratekit.core.exit_codes import Remedy as _Canonical

Remedy = __import__("enum").StrEnum("Remedy", {m.name: m.value.replace("run-setup", "run-set-up") for m in _Canonical})

```

### `r301.V4_label_shape_loose`

A host label may hold anything, so a scheme, a path or a port passes

- File: `src/cratekit/core/config_schema.py`
- Source: `r301.json`, row `V4_label_shape_loose`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[-bad.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[Identify-EU-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[https://identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify eu.acrcloud.com]`

Old text:

```
_HOST_LABEL = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
```

New text:

```
_HOST_LABEL = re.compile(r"^.+$")
```

### `r345.A1_colon_required`

backup_remote_name: accept a value with no colon, so a bare folder name names a remote (the brief's row)

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A1_colon_required`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_destination_keys_are_published_for_the_wizard_and_the_verb`

Old text:

```
    if not colon or len(name) < 2:
        return None
```

New text:

```
    if len(name) < 2:
        return None
```

### `r345.A2_single_letter`

backup_remote_name: accept a single character before the colon, so C:/x names a remote called C

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A2_single_letter`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-dest]`

Old text:

```
    if not colon or len(name) < 2:
        return None
```

New text:

```
    if not colon or len(name) < 1:
        return None
```

### `r345.A3_name_shape`

backup_remote_name: drop the rclone name rule, so -gdrive and a trailing space name a remote

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A3_name_shape`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-dest]`

Old text:

```
    if not _RCLONE_REMOTE_NAME.match(name):
        return None
```

New text:

```
    if False:
        return None
```

### `r345.A4_leading_hyphen`

the name rule admits a leading hyphen

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A4_leading_hyphen`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`

Old text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")
```

New text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@-][\w.+@ -]*(?<! )$")
```

### `r345.A5_trailing_space`

the name rule admits a trailing space

- File: `src/cratekit/core/config_schema.py`
- Source: `r345.json`, row `A5_trailing_space`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[gdrive :bucket-dest]`

Old text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*(?<! )$")
```

New text:

```
_RCLONE_REMOTE_NAME = re.compile(r"^[\w.+@][\w.+@ -]*$")
```

### `r44-a.C3_identity_not_written`

Never write a rule's identity back out, so a saved configuration loses it

- File: `src/cratekit/core/config_schema.py`
- Source: `r44-a.json`, row `C3_identity_not_written`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`

Old text:

```
        if PREFIX_VOLUME_IDENTITY_KEY in out:
```

New text:

```
        if False:
```

### `r662-a.M2_spelled_path_compared_whole`

the spelled remote is compared whole rather than by its name, so gdrive: beside gdrive destinations reads as a disagreement

- File: `src/cratekit/core/config_schema.py`
- Source: `r662-a.json`, row `M2_spelled_path_compared_whole`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:]`
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:bucket]`

Old text:

```
    if remote.split(":", 1)[0] == expected:
        return None
    return remote, expected
```

New text:

```
    if remote == expected:
        return None
    return remote, expected
```

### `r662-b.M1b_several_remotes_compared`

M1 again after the round's test: destinations naming several remotes are compared against the spelled remote anyway

- File: `src/cratekit/core/config_schema.py`
- Source: `r662-b.json`, row `M1b_several_remotes_compared`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if len(named) != 1:
        return None
    expected = next(iter(named))
```

New text:

```
    if not named:
        return None
    expected = next(iter(named))
```

### `r662-b.M3b_blank_remote_disagrees`

M3 again after the round's test: a blank spelled remote is no longer treated as unset

- File: `src/cratekit/core/config_schema.py`
- Source: `r662-b.json`, row `M3b_blank_remote_disagrees`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if not isinstance(remote, str) or not remote.strip():
        return None
    named = {
```

New text:

```
    if not isinstance(remote, str):
        return None
    named = {
```

### `u197-m6.M6_composite`

What the default does hold: default to the alternative, a name the fold leaves alone, so a fresh configuration selects streamrip

- File: `src/cratekit/core/config_schema.py`
- Source: `u197-m6.json`, row `M6_composite`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_vendored_adapter_is_the_default_under_its_neutral_name`

Old text:

```
    adapter: str = "vendored"
```

New text:

```
    adapter: str = "streamrip"
```

### `u197.M2_retired_mapping_empty`

RETIRED_ADAPTER_NAMES: forget the vendored downloader's old key, so an older configuration names an unknown adapter

- File: `src/cratekit/core/config_schema.py`
- Source: `u197.json`, row `M2_retired_mapping_empty`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_config.py::test_only_a_retired_adapter_key_is_folded`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({"tidal_dl_ng": "vendored"})
```

New text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({})
```

### `u233.C1_schema_default_moves`

config: labels.offer_per_sweep's default goes from 10 to 12, so the guide's settings table states an old default

- File: `src/cratekit/core/config_schema.py`
- Source: `u233.json`, row `C1_schema_default_moves`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
DEFAULT_LABEL_OFFER = 10
```

New text:

```
DEFAULT_LABEL_OFFER = 12
```

### `u233.C2_schema_gains_a_key`

config: LabelsConfig gains a key a person can set, which the guide's settings table has no row for

- File: `src/cratekit/core/config_schema.py`
- Source: `u233.json`, row `C2_schema_gains_a_key`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_docs_current.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_docs_current.py::test_the_settings_table_is_the_schema`

Old text:

```
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS

```

New text:

```
    new_playlist_age_days: int = DEFAULT_NEW_PLAYLIST_AGE_DAYS
    sweep_note_days: int = 3

```

### `u299.U12_pin_refusal_remedy`

Config.assert_rekordbox_pin_recorded: the refusal moved behind a local import tells a person to fix the values, not record the pin

- File: `src/cratekit/core/config_schema.py`
- Source: `u299.json`, row `U12_pin_refusal_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_unset_rekordbox_pin_refuses_to_write_with_its_own_remedy`

Old text:

```
                remedy=Remedy.RECORD_REKORDBOX_PIN,
```

New text:

```
                remedy=Remedy.FIX_CONFIG_VALUES,
```

### `u331.S04_membership_ignores_explicit_toggles`

Config.membership: resolve the profile's preset alone, so a toggle the configuration turns on or off is ignored where a feature package reads the membership

- File: `src/cratekit/core/config_schema.py`
- Source: `u331.json`, row `S04_membership_ignores_explicit_toggles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_membership_is_the_profiles_preset_then_the_explicit_toggles`

Old text:

```
        """The resolved membership: the profile's preset, then the explicit toggles."""
        return profiles.resolve(self.profile.name, self.modules.explicit)
```

New text:

```
        """The resolved membership: the profile's preset, then the explicit toggles."""
        return profiles.resolve(self.profile.name, {})
```

### `r227.V1_validator_not_called`

validate never asks about outbound.export_stale_days

- File: `src/cratekit/core/config_validate.py`
- Source: `r227.json`, row `V1_validator_not_called`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_an_export_staleness_nobody_could_mean_is_refused_with_its_ceiling`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[-3]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[0]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[2.5]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[True]`
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[seven]`

Old text:

```
    problems += _validate_export_staleness(data)

```

New text:

```
(empty)
```

### `r227.V2_no_ceiling`

The key has no ceiling, so ten billion days validates and overflows later

- File: `src/cratekit/core/config_validate.py`
- Source: `r227.json`, row `V2_no_ceiling`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_export_staleness_nobody_could_mean_is_refused_with_its_ceiling`

Old text:

```
        maximum=MAX_EXPORT_STALE_DAYS,
```

New text:

```
        maximum=None,
```

### `r227.V3_bool_is_a_day_count`

The shared day count rule accepts a boolean, for the intake ages as well

- File: `src/cratekit/core/config_validate.py`
- Source: `r227.json`, row `V3_bool_is_a_day_count`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_export_staleness_that_is_not_a_positive_day_count_is_refused[True]`

Old text:

```
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        return (
```

New text:

```
    if not isinstance(value, int) or value < 1:
        return (
```

### `r301.V1_validator_not_called`

validate never checks the recognition section

- File: `src/cratekit/core/config_validate.py`
- Source: `r301.json`, row `V1_validator_not_called`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 17 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[-bad.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[7]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[Identify-EU-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com.example]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[evilacrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[https://identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify eu.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com.attacker.example]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com/v1/identify]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com:443]`
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[-3]`
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[0]`
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[2.5]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    problems += _validate_recognition(data)

```

New text:

```
(empty)
```

### `r301.V2_any_domain`

The host may sit under any domain, so the credential can travel anywhere

- File: `src/cratekit/core/config_validate.py`
- Source: `r301.json`, row `V2_any_domain`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com.example]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[evilacrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com.attacker.example]`

Old text:

```
    if not all(_HOST_LABEL.match(label) for label in labels) or not value.endswith(
        f".{RECOGNITION_HOST_DOMAIN}"
    ):
```

New text:

```
    if not all(_HOST_LABEL.match(label) for label in labels):
```

### `r301.V3_suffix_without_dot`

The domain is checked as a bare suffix, so evilacrcloud.com passes

- File: `src/cratekit/core/config_validate.py`
- Source: `r301.json`, row `V3_suffix_without_dot`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[evilacrcloud.com]`

Old text:

```
        f".{RECOGNITION_HOST_DOMAIN}"
```

New text:

```
        f"{RECOGNITION_HOST_DOMAIN}"
```

### `r301.V6_bool_is_a_bound`

A boolean monthly bound is accepted, so true reads as one call a month

- File: `src/cratekit/core/config_validate.py`
- Source: `r301.json`, row `V6_bool_is_a_bound`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[True]`

Old text:

```
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 1
    ):
```

New text:

```
        not isinstance(bound, int) or bound < 1
    ):
```

### `r301.V7_zero_is_a_bound`

A zero monthly bound is accepted, which refuses every paid call

- File: `src/cratekit/core/config_validate.py`
- Source: `r301.json`, row `V7_zero_is_a_bound`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[0]`

Old text:

```
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 1
    ):
```

New text:

```
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 0
    ):
```

### `r345.A10_spelled_remote_wins`

derived_backup_remote: derive even when the file spells a remote, so the file's own spelling is overwritten

- File: `src/cratekit/core/config_validate.py`
- Source: `r345.json`, row `A10_spelled_remote_wins`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 9 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:]`
  - `tests/test_config.py::test_a_spelled_backup_remote_that_matches_the_destinations_is_kept[gdrive:bucket]`
  - `tests/test_config.py::test_the_destination_keys_are_published_for_the_wizard_and_the_verb`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-absent]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-it]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-unreadable]`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_keeps_recorded_backup_destinations_without_asking`

Old text:

```
    if isinstance(remote, str) and remote.strip():
        return None
    for key in BACKUP_DESTINATION_KEYS:
```

New text:

```
    if False:
        return None
    for key in BACKUP_DESTINATION_KEYS:
```

### `r345.A6_one_remote`

_validate_backup_destinations: let the three destinations name several remotes

- File: `src/cratekit/core/config_validate.py`
- Source: `r345.json`, row `A6_one_remote`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_the_backup_destinations_must_name_one_remote`
  - `tests/test_doctor.py::test_no_disagreement_is_read_where_there_is_nothing_to_compare`

Old text:

```
    if len(set(named.values())) > 1:
```

New text:

```
    if len(set(named.values())) > 3:
```

### `r345.A8_validate_wiring`

validate: do not call the backup destination check at all

- File: `src/cratekit/core/config_validate.py`
- Source: `r345.json`, row `A8_validate_wiring`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 30 (killed)
- Killed:
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[-gdrive:bucket-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[:local:/tmp/backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[:local:/tmp/backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[:local:/tmp/backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:/Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[C:\\Backups-dest]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[MusicBackup-archive_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[MusicBackup-db_dest_root]`
  - `tests/test_config.py::test_a_backup_destination_naming_no_remote_is_refused[MusicBackup-dest]`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    problems += _validate_backup_destinations(data)

```

New text:

```
(empty)
```

### `r44-a.C1_rule_identity_may_be_a_path`

Accept a mount path as a rule's volume identity

- File: `src/cratekit/core/config_validate.py`
- Source: `r44-a.json`, row `C1_rule_identity_may_be_a_path`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[drive-path]`
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[posix-path]`
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[unc-path]`

Old text:

```
                problems += _mount_path_problem(key, identity)
```

New text:

```
                pass
```

### `r44-a.C2_blank_identity_is_absence`

Read a blank rule identity as none recorded instead of as a problem

- File: `src/cratekit/core/config_validate.py`
- Source: `r44-a.json`, row `C2_blank_identity_is_absence`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[blank]`
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[empty]`

Old text:

```
            if not isinstance(identity, str) or not identity.strip():
```

New text:

```
            if not isinstance(identity, str):
```

### `r662-a.M4_validator_drops_disagreement`

the validator no longer reports a spelled remote the destinations disagree with

- File: `src/cratekit/core/config_validate.py`
- Source: `r662-a.json`, row `M4_validator_drops_disagreement`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 7 (killed)
- Killed:
  - `tests/test_config.py::test_a_spelled_backup_remote_that_names_another_remote_is_refused`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-absent]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-it]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-knows-neither]`
  - `tests/test_doctor.py::test_a_spelled_remote_is_kept_unless_rclone_was_read_and_lacks_it[rclone-unreadable]`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_setup_token_stays_when_the_disagreement_is_not_the_only_problem`

Old text:

```
    disagreement = backup_remote_disagreement(data)
    if disagreement is not None:
```

New text:

```
    disagreement = backup_remote_disagreement(data)
    if False:
```

### `r662-a.M5_validator_message_loses_flag`

the validator's problem text no longer names the flag, reworded rather than truncated

- File: `src/cratekit/core/config_validate.py`
- Source: `r662-a.json`, row `M5_validator_message_loses_flag`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`

Old text:

```
Setup's --backup-remote replaces the "
            f"spelled one (R-662)."
```

New text:

```
Setup can be run again to "
            f"change it (R-662)."
```

### `r744.C1_equal_bounds_accepted`

a floor equal to the ceiling is accepted, an empty window the estimator answers None for on every track

- File: `src/cratekit/core/config_validate.py`
- Source: `r744.json`, row `C1_equal_bounds_accepted`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_an_empty_or_ill_typed_window_is_refused_at_load[analysis0-must be below]`

Old text:

```
    if isinstance(floor, int) and isinstance(ceiling, int) and floor >= ceiling:
```

New text:

```
    if isinstance(floor, int) and isinstance(ceiling, int) and floor > ceiling:
```

### `r744.C2_bool_accepted`

a boolean is accepted as a bound, since bool is an int to isinstance

- File: `src/cratekit/core/config_validate.py`
- Source: `r744.json`, row `C2_bool_accepted`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`
- Collected: 65 against a baseline of 65
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_an_empty_or_ill_typed_window_is_refused_at_load[analysis5-tempo_floor must be a whole number]`

Old text:

```
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
```

New text:

```
        if not isinstance(value, int) or value < 1:
```

### `r790-c.C1_config_floor`

_validate_labels: accept zero

- File: `src/cratekit/core/config_validate.py`
- Source: `r790-c.json`, row `C1_config_floor`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_configured_offer_must_be_a_positive_whole_number[0]`

Old text:

```
        not isinstance(offer, int) or isinstance(offer, bool) or offer < 1
```

New text:

```
        not isinstance(offer, int) or isinstance(offer, bool) or offer < 0
```

### `u117-operator.D13_config_validation`

config: accept a zero age

- File: `src/cratekit/core/config_validate.py`
- Source: `u117-operator.json`, row `D13_config_validation`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_dated.py::test_the_age_key_defaults_to_thirty_and_refuses_zero`

Old text:

```
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 1):
```

New text:

```
    if age is not None and (not isinstance(age, int) or isinstance(age, bool) or age < 0):
```

### `u157.F1_cut_zero`

_validate_drift_cut: accept a cut of zero, which marks every measured track

- File: `src/cratekit/core/config_validate.py`
- Source: `u157.json`, row `F1_cut_zero`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_drift.py::test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load[0.0]`
  - `tests/test_drift.py::test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load[0]`

Old text:

```
        or value <= 0
        or value > 100
```

New text:

```
        or value < 0
        or value > 100
```

### `u157.F2_cut_nan`

_validate_drift_cut: accept a cut that is not finite

- File: `src/cratekit/core/config_validate.py`
- Source: `u157.json`, row `F2_cut_nan`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_cut_that_is_not_a_percent_above_zero_is_refused_at_load[nan]`

Old text:

```
        or not math.isfinite(value)
        or value <= 0
```

New text:

```
        or value <= 0
```

### `u197.M1_config_fold`

_acquisition: return the section as written, so a file naming the retired key reaches doctor and every report under it

- File: `src/cratekit/core/config_validate.py`
- Source: `u197.json`, row `M1_config_fold`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
    current = current_adapter_name(built.adapter)
    if current == built.adapter:
        return built
```

New text:

```
    current = current_adapter_name(built.adapter)
    if True:
        return built
```

### `u206.M22_days_validation_dropped`

_validate_provider: accept a negative isrc_cache_days

- File: `src/cratekit/core/config_validate.py`
- Source: `u206.json`, row `M22_days_validation_dropped`
- Moved: the same text, now in src/cratekit/core/config_validate.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_days_value_that_is_not_a_whole_number_of_days_is_refused[-1]`

Old text:

```
    if days is not None and (not isinstance(days, int) or isinstance(days, bool) or days < 0):
```

New text:

```
    if days is not None and (not isinstance(days, int) or isinstance(days, bool)):
```

### `u241.M09_ceiling_ignores_the_reserve`

worker_ceiling: every core, nothing kept back for the driver

- File: `src/cratekit/core/cores.py`
- Source: `u241.json`, row `M09_ceiling_ignores_the_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cores.py`
- Collected: 42 against a baseline of 42
- Kills: 7 (killed)
- Killed:
  - `tests/test_cores.py::test_a_ceiling_from_many_cores_never_widens_what_memory_affords`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[11-2-9]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[2-2-1]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[3-2-1]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[4-2-2]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[8-1-7]`
  - `tests/test_cores.py::test_the_reader_is_looked_up_when_called_so_a_test_can_stand_in`

Old text:

```
    return max(1, cores - reserved)

```

New text:

```
    return max(1, cores)

```

### `u93-recursive-analysis.D10_sorted_items`

Return the items in walk order rather than sorted

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D10_sorted_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[nested-every-file-once-sorted]`

Old text:

```
        items=tuple(sorted(items)),
```

New text:

```
        items=tuple(items),
```

### `u93-recursive-analysis.D11_absolute_id`

Drop the absolute clause from item_path, so an absolute id discards the frozen folder

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D11_absolute_id`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_an_absolute_id_is_refused_rather_than_discarding_the_folder`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
```

New text:

```
    if ".." in candidate.parts:
```

### `u93-recursive-analysis.D12_parent_id`

Drop the dot dot clause from item_path, so an id walks out of the frozen folder

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D12_parent_id`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_parent_segment_is_refused`
  - `tests/test_discovery.py::test_the_refusal_names_the_folder_it_was_leaving`

Old text:

```
    if candidate.is_absolute() or ".." in candidate.parts:
        raise _escapes(folder, item_id)
```

New text:

```
    if candidate.is_absolute():
        raise _escapes(folder, item_id)
```

### `u93-recursive-analysis.D13_singular`

Drop the singular branch, so one declined folder reads as 1 folders

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D13_singular`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`

Old text:

```
    return f"{count} folder" if count == 1 else f"{count} folders"
```

New text:

```
    return f"{count} folders"
```

### `u93-recursive-analysis.D15_unreadable_empty`

unreadable_warning reports over an empty list, the same false omission on the other code

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D15_unreadable_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 6 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`

Old text:

```
    """What a recursive walk could not list, phrased for an envelope."""
    if not paths:
        return None

```

New text:

```
    """What a recursive walk could not list, phrased for an envelope."""

```

### `u93-recursive-analysis.D16_none_filter`

walk_warnings stops dropping the Nones, so an envelope carries a null warning

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D16_none_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 9 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_from_a_build_that_never_walked_a_tree_says_nothing`
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`
  - `tests/test_discovery.py::test_a_resume_repeats_the_unreadable_half_and_not_only_the_links`
  - `tests/test_discovery.py::test_a_resume_says_what_the_queue_said_from_the_payload_alone`
  - `tests/test_discovery.py::test_an_error_carrying_no_filename_is_still_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_unreadable_warning_is_its_own_code_with_its_own_remedy`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`
  - `tests/test_discovery.py::test_there_is_nothing_to_say_when_no_link_was_declined`

Old text:

```
    return tuple(one for one in said if one is not None)
```

New text:

```
    return said
```

### `u93-recursive-analysis.D17_and_more`

Drop the and N more tail, so a warning names five and silently omits the rest

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D17_and_more`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`

Old text:

```
    return ", ".join(shown) + (f", and {rest} more" if rest else "")
```

New text:

```
    return ", ".join(shown)
```

### `u93-recursive-analysis.D18_strings_shape`

Drop the shape check on a frozen payload list, so a string payload is read character by character

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D18_strings_shape`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_payload_whose_lists_are_the_wrong_shape_says_nothing_rather_than_raising`

Old text:

```
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(one) for one in value)
```

New text:

```
    return tuple(str(one) for one in value or ())
```

### `u93-recursive-analysis.D19_resume_half`

warnings_of reads only the links, so an unreadable folder is on the queue and never on the resume

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D19_resume_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_resume_repeats_the_unreadable_half_and_not_only_the_links`

Old text:

```
    return walk_warnings(
        _strings(held.get(PAYLOAD_SKIPPED_LINKS)),
        _strings(held.get(PAYLOAD_UNREADABLE)),
    )
```

New text:

```
    return walk_warnings(_strings(held.get(PAYLOAD_SKIPPED_LINKS)))
```

### `u93-recursive-analysis.D1_dotfile`

Drop the dotfile clause from _is_audio, which is what lets an AppleDouble sidecar become an item

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D1_dotfile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[appledouble-sidecar-skipped]`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
```

New text:

```
        path.is_file()
        and path.suffix.lower() in AUDIO_EXTS
```

### `u93-recursive-analysis.D20_frozen_links`

frozen stops recording the declined links, so the resume has nothing to read back

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D20_frozen_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`

Old text:

```
        PAYLOAD_SKIPPED_LINKS: list(scan.skipped_links),
```

New text:

```
        PAYLOAD_SKIPPED_LINKS: [],
```

### `u93-recursive-analysis.D2_is_file`

is_file becomes exists, so a directory named track.flac becomes an item

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D2_is_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_directory_carrying_an_audio_suffix_is_not_an_item`

Old text:

```
        path.is_file()
        and not path.name.startswith(".")
```

New text:

```
        path.exists()
        and not path.name.startswith(".")
```

### `u93-recursive-analysis.D3_suffix`

Drop the audio suffix clause, so cover art and text files become items

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D3_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[non-audio-suffix]`

Old text:

```
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
    )
```

New text:

```
        and not path.name.startswith(".")
    )
```

### `u93-recursive-analysis.D4_default_mode`

Drop the one level early return, so every caller walks the tree whether it asked or not

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D4_default_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_one_level_scan_reports_no_links_even_when_one_is_there`
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[one-level-default-skips-a-subfolder]`

Old text:

```
    if not recursive:
        return Scan(
            items=tuple(sorted(path.name for path in folder.iterdir() if _is_audio(path))),
            skipped_links=(),
            unreadable=(),
        )

```

New text:

```
(empty)
```

### `u93-recursive-analysis.D5_dot_directory`

Stop pruning dot directories, so .Trashes and .Spotlight-V100 are walked

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D5_dot_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[dot-directory-not-descended]`

Old text:

```
            if name.startswith("."):
                continue
            if (here / name).is_symlink():
```

New text:

```
            if (here / name).is_symlink():
```

### `u93-recursive-analysis.D6_link_declined`

Walk a directory symlink and report nothing, which is the loop hazard and the silent skip at once

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D6_link_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 4 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_symlinked_directory_is_not_walked_and_is_reported`
  - `tests/test_discovery.py::test_one_declined_link_reads_as_one_folder_and_not_as_one_folders`
  - `tests/test_discovery.py::test_the_frozen_payload_carries_the_mode_and_both_omissions`
  - `tests/test_discovery.py::test_the_warning_names_the_links_and_counts_the_rest`

Old text:

```
            if (here / name).is_symlink():
                skipped.append(_relative(folder, here / name))
                continue
            kept.append(name)
```

New text:

```
            kept.append(name)
```

### `u93-recursive-analysis.D7_prune_in_place`

Assign the filtered list to a new name instead of the slice, which leaves os.walk descending everything

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D7_prune_in_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_discovery.py::test_a_scan_holds_exactly_the_audio_files_it_should[dot-directory-not-descended]`

Old text:

```
        dirnames[:] = kept
```

New text:

```
        dirnames = kept  # noqa: F841
```

### `u93-recursive-analysis.D9_onerror`

Drop the error callback, so an unreadable folder contributes nothing and is never named

- File: `src/cratekit/core/discovery.py`
- Source: `u93-recursive-analysis.json`, row `D9_onerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discovery.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
os.walk(root, followlinks=False, onerror=note)
```

New text:

```
os.walk(root, followlinks=False)
```

### `u329.R2_run_setup_token_text`

the one home's run setup token is spelled differently, which config.Remedy now reads too

- File: `src/cratekit/core/exit_codes.py`
- Source: `u329.json`, row `R2_run_setup_token_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_update.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_config_update.py::test_two_wizards_answering_one_key_differently_refuse_and_write_nothing`

Old text:

```
    RUN_SETUP = "run-setup"
```

New text:

```
    RUN_SETUP = "run-set-up"
```

### `u185.F11_difference_memberships`

differences: compare no membership rows, so raw SQL on a pushed membership passes

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F11_difference_memberships`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
        if old == new:
            continue
```

New text:

```
        if True:
            continue
```

### `u185.F12_difference_appeared`

differences: read a row that appeared in the folder since open as nothing

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F12_difference_appeared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`

Old text:

```
            found.append(f"the {_PLAYLISTS} row {key!r} appeared under {OWNER}'s folder")
```

New text:

```
            pass
```

### `u185.F1_root_must_be_a_folder`

is_foreign_root: drop the folder test, so a plain playlist named DEADCA7 at the top is foreign

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F1_root_must_be_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 4 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-0-a plain playlist of the name is not the shape the push writes]`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-4-a smart playlist of the name is not either]`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-None-a row that cannot say it is a folder is not one]`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-root-x-nor one whose kind is not a number]`

Old text:

```
    return folder and str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()
```

New text:

```
    return str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()
```

### `u185.F2_root_must_be_at_the_top`

is_foreign_root: drop the root parent test, so a namesake folder below the top is foreign

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F2_root_must_be_at_the_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_foreign_tree.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_foreign_tree.py::test_every_node_under_the_root_is_foreign_at_any_depth_and_nothing_beside_it`
  - `tests/test_foreign_tree.py::test_nothing_else_is_a_foreign_root[DEADCA7-12-1-a folder of the name below the top is a namesake]`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`

Old text:

```
    return folder and str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()
```

New text:

```
    return folder and str(name) in FOREIGN_ROOT_NAMES
```

### `u185.F3_descendants_walked`

ids_of: walk no children, so only the root row is foreign and its playlists are anyone's

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F3_descendants_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_foreign_tree.py`, `tests/test_genre_favorites.py`
- Collected: 144 against a baseline of 144
- Kills: 9 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_foreign_tree.py::test_a_cycle_ends_the_walk_rather_than_looping`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_every_node_under_the_root_is_foreign_at_any_depth_and_nothing_beside_it`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`
  - `tests/test_genre_favorites.py::test_a_source_namesake_inside_deadca7s_folder_is_not_a_second_source`

Old text:

```
        queue.extend(children.get(node, ()))
```

New text:

```
        pass
```

### `u185.F4_create_inside`

pending_touches: admit a playlist created inside the folder

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F4_create_inside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`

Old text:

```
            if op == "create" and parent in ids:
```

New text:

```
            if op == "create" and parent in ids and False:
```

### `u185.F5_second_root`

pending_touches: admit a second DEADCA7 folder created at the top

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F5_second_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`

Old text:

```
            elif op == "create" and is_foreign_root(
```

New text:

```
            elif op == "create" and False and is_foreign_root(
```

### `u185.F7_modify_inside`

pending_touches: admit any change to a row of the folder

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F7_modify_inside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[folder-renamed]`

Old text:

```
            elif op == "modify" and key in ids:
```

New text:

```
            elif op == "modify" and key in ids and False:
```

### `u185.F8_moved_in`

pending_touches: admit a node of one's own moved into the folder

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F8_moved_in`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`

Old text:

```
            elif op == "modify" and parent in ids:
```

New text:

```
            elif op == "modify" and parent in ids and False:
```

### `u185.F9_membership`

pending_touches: read a membership by its owner alone, so one rewritten to another playlist passes

- File: `src/cratekit/core/foreign_tree.py`
- Source: `u185.json`, row `F9_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`

Old text:

```
            if owner in ids or str(getattr(obj, "ID", "")) in reading.memberships:
```

New text:

```
            if owner in ids:
```

### `r289-b.D1_no_chunking`

Ask about every name in one statement, past the parameter limit

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D1_no_chunking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_states_of_answers_past_the_parameter_limit_of_one_statement`

Old text:

```
_ID_CHUNK = 500
```

New text:

```
_ID_CHUNK = 1_000_000
```

### `r289-b.D3_unknown_name_gets_a_state`

Answer for every name asked about, inventing queued for the unknown ones

- File: `src/cratekit/core/jobs.py`
- Source: `r289-b.json`, row `D3_unknown_name_gets_a_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_states_of_answers_for_the_names_it_knows_and_omits_the_rest`
  - `tests/test_jobs.py::test_states_of_answers_past_the_parameter_limit_of_one_statement`

Old text:

```
    found: dict[str, JobState] = {}
    wanted = list(job_ids)
```

New text:

```
    wanted = list(job_ids)
    found: dict[str, JobState] = dict.fromkeys(wanted, JobState.QUEUED)
```

### `r290-author.J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J1_blocked_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 44 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`
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
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.import]`
  - ... and 29 more, see the JSON sidecar

Old text:

```
    if job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

New text:

```
    if False and job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

### `r290-author.J2_blocked_raises_the_plain_type`

Raise a plain CratekitError for a parked job, so the verb exits non zero and the outcome word says failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J2_blocked_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 43 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
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
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.judge]`
  - ... and 28 more, see the JSON sidecar

Old text:

```
        raise JobBlocked(job.cause)
```

New text:

```
        raise CratekitError(job.cause)
```

### `r290-author.J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J3_closed_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 62 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - ... and 47 more, see the JSON sidecar

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
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 21 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - ... and 6 more, see the JSON sidecar

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

### `r290-author.J5_causeless_block_returns`

Return for a blocked job that records no reason, reading a missing reason as a missing problem

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J5_causeless_block_returns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`

Old text:

```
        if job.cause is None:
            raise JobBlocked(
                refuse(
```

New text:

```
        if job.cause is None:
            return
            raise JobBlocked(
                refuse(
```

### `r290-author.J6_causeless_block_raises_the_plain_type`

Refuse a blocked job that records no reason as a plain error, so the envelope says failed over a row the job listing calls blocked

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J6_causeless_block_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`

Old text:

```
        if job.cause is None:
            raise JobBlocked(
                refuse(
```

New text:

```
        if job.cause is None:
            raise CratekitError(
                refuse(
```

### `r290-author.J7_cancelled_raises_the_plain_type`

Raise a plain CratekitError for a cancelled job, so a person who stopped a run is told it failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J7_cancelled_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 21 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            raise JobCancelled(job.cause)
```

New text:

```
            raise CratekitError(job.cause)
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Moved: Anchored where u325-replay-after.json replayed it: U298 replaced the resume tails of tagging.shell.advance, adopt.shell.advance, acquire fallback-fetch and master with core.jobs.resumed, which advance calls; its one raise_for_state call is the mapping each of those four shells made, and tests/test_job_outcome.py names that function as the shared tail. The tests are this row's own plus those of the three rows mapped to it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 33 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[label.judge]`
  - ... and 18 more, see the JSON sidecar

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
- Ran: `tests/test_jobs.py`
- Collected: 0 against a baseline of 84
- Kills: 0 (error)
- Note: OSError: [Errno 39] Directory not empty: 'pytest-0'

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
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

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

### `r390-a.A3_a_failed_job_with_no_cause_is_refused`

a missing verdict is read as a permanent one

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A3_a_failed_job_with_no_cause_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_failed_job_with_no_recorded_cause_still_re_arms`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is None or not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

### `r390-a.A4_refusal_drops_the_permanent_reasons`

the resume refusal no longer names the mixed reasons at its own top level

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A4_refusal_drops_the_permanent_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
```

New text:

```
                "state": str(current.state),
            },
            inner=current.cause,
```

### `r390-a.A5_refusal_drops_the_inner_cause`

the refusal no longer nests the job's own cause, so the item's reason is unreachable

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A5_refusal_drops_the_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`

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

### `r390-b.B6_envelope_drops_the_reasons`

the all failed envelope keeps the item nested and drops the reasons beside it

- File: `src/cratekit/core/jobs.py`
- Source: `r390-b.json`, row `B6_envelope_drops_the_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
        message += (
            f"; the failures carry {len(permanent_reasons)} distinct permanent "
            f"reasons: {', '.join(permanent_reasons)}"
        )
        detail[PERMANENT_REASONS] = tuple(permanent_reasons)
```

New text:

```
        pass
```

### `u140.B3_refreeze_any_state`

jobs.refreeze drops the succeeded state check, so a job that may still run is rewritten

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B3_refreeze_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_refreeze_refuses_a_job_that_has_not_succeeded`

Old text:

```
        if current.state is not JobState.SUCCEEDED:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

New text:

```
        if False:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "

```

### `u140.B4_refreeze_writes_nothing_new`

jobs.refreeze writes the payload back without the new value

- File: `src/cratekit/core/jobs.py`
- Source: `u140.json`, row `B4_refreeze_writes_nothing_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        payload[key] = str(value)

```

New text:

```
        payload.setdefault(key, str(value))

```

### `u235.S1_enqueue_ignores_a_given_job_id`

jobs.enqueue: a job id the caller names is ignored and a fresh identifier minted, a sample of the guard that hands new_run_id to every job

- File: `src/cratekit/core/jobs.py`
- Source: `u235.json`, row `S1_enqueue_ignores_a_given_job_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 26 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[job-id-beside-stale-days]`
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[negative-days]`
  - `tests/test_jobs.py::test_a_bad_stale_cancel_is_the_parsers_usage_error_and_cancels_nothing[zero-days]`
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`
  - `tests/test_jobs.py::test_a_cancelled_stale_job_reports_cancelled_and_resumes_by_its_own_command`
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_a_dry_run_of_one_job_cancels_nothing`
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`
  - `tests/test_jobs.py::test_a_running_job_is_never_listed_for_cancel_however_old`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[another-open-job-holds-it]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[unparseable-url]`
  - `tests/test_jobs.py::test_a_stale_cancel_says_what_it_frees[url-typed-by-hand-holds-the-swept-id]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[hearts-job]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[set-job]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    identifier = job_id or new_run_id()
```

New text:

```
    identifier = new_run_id()
```

### `u270.J1_claim_batch_size_floor`

claim_batch: accept a batch of zero items, so a size the binding never checks claims nothing and the job reads as finished

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J1_claim_batch_size_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_claim_batch_refuses_a_batch_of_no_items[0]`

Old text:

```
    if limit < 1:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
```

New text:

```
    if limit < 0:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
```

### `u270.J2_claim_batch_order`

claim_batch: claim the highest ordinals first, so a batch writes its tracks in the reverse of the crate's order

- File: `src/cratekit/core/jobs.py`
- Source: `u270.json`, row `J2_claim_batch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 8 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`
  - `tests/test_jobs_batch.py::test_a_batch_is_claimed_in_ordinal_order_up_to_its_size`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`
  - `tests/test_jobs_batch.py::test_a_signal_after_one_batch_keeps_it_done_and_claims_no_other`
  - `tests/test_jobs_batch.py::test_claim_batch_takes_only_pending_items_and_none_when_nothing_is_left`
  - `tests/test_jobs_batch.py::test_every_item_of_a_batch_is_held_claimed_while_its_handler_runs`

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
- Ran: `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`
- Collected: 183 against a baseline of 183
- Kills: 45 (killed)
- Killed:
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_that_files_a_favourite_puts_it_in_its_folders_favorites`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_with_no_source_playlist_files_its_tracks_and_says_the_refresh_skipped`
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_job_that_finished_reports_the_same_counts_when_asked_again`
  - ... and 30 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `u301.J1_job_row_answers_none`

_job_row: answer None for an unknown job instead of refusing, so get, refreeze and join_run fail on an attribute rather than job-unknown

- File: `src/cratekit/core/jobs.py`
- Source: `u301.json`, row `J1_job_row_answers_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_an_unknown_job_refuses_with_a_code_from_the_vocabulary`
  - `tests/test_jobs.py::test_every_job_verb_refuses_an_unknown_identifier_with_the_same_code`

Old text:

```
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None:
        raise refuse(
            "job-unknown",
```

New text:

```
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None and False:
        raise refuse(
            "job-unknown",
```

### `u301.J2_release_claims_any_driver`

release_claims: release every driver's claims when one driver is named, so a parked driver frees an item a second driver holds

- File: `src/cratekit/core/jobs.py`
- Source: `u301.json`, row `J2_release_claims_any_driver`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_releasing_one_drivers_claims_leaves_another_drivers_claim`

Old text:

```
    if driver is not None:
        query += " AND claimed_by = ?"
        params += (driver,)
```

New text:

```
    if False:
        query += " AND claimed_by = ?"
        params += (driver,)
```

### `r380.G3_retryable_requires_every_item`

a mixed job is non retryable unless every failure is retryable

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r380.json`, row `G3_retryable_requires_every_item`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_failures_include_a_retryable_cause_stays_retryable`

Old text:

```
    if not failed or any(cause.retryable for cause in failed):

```

New text:

```
    if not failed or all(cause.retryable for cause in failed):

```

### `r380.G5_permanent_failures_still_offer_resume`

the permanent branch still carries the resume-job remedy

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r380.json`, row `G5_permanent_failures_still_offer_resume`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[three-items]`
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[two-items]`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

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

### `r390-b.B1_last_reason_restored`

the original defect: several permanent reasons take the last item's reason

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B1_last_reason_restored`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
    reason = reasons[0] if len(reasons) == 1 else "mixed-permanent-failures"
```

New text:

```
    reason = failed[-1].reason
```

### `r390-b.B2_reasons_in_reverse_order`

the sorted set is pinned in one order: reverse it

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B2_reasons_in_reverse_order`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
    reasons = tuple(sorted({cause.reason for cause in failed}))
```

New text:

```
    reasons = tuple(sorted({cause.reason for cause in failed}, reverse=True))
```

### `r390-b.B3_message_does_not_name_the_reasons`

the job cause message keeps the counts and drops the list of reasons

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B3_message_does_not_name_the_reasons`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
            detail[PERMANENT_REASONS] = reasons
```

New text:

```
            detail[PERMANENT_REASONS] = reasons
```

### `r390-b.B4_detail_drops_permanent_reasons`

the job cause names the reasons in prose and drops them from detail

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B4_detail_drops_permanent_reasons`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
            detail[PERMANENT_REASONS] = reasons
```

New text:

```
            message += (
                f"; the {permanent} permanent failures carry {len(reasons)} "
                f"distinct reasons: {', '.join(reasons)}"
            )
```

### `r390-b.B5_one_shared_reason_is_also_mixed`

the threshold moves so a single shared reason is reported as mixed too

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B5_one_shared_reason_is_also_mixed`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[three-items]`
  - `tests/test_jobs.py::test_a_job_whose_every_item_failed_permanently_reports_itself_non_retryable[two-items]`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`

Old text:

```
        if len(reasons) > 1:
            # R-391.
```

New text:

```
        if len(reasons) > 0:
            # R-391.
```

### `r390-b.B7_drive_passes_no_reasons_to_the_envelope`

the envelope can carry the reasons and the driver hands it none

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r390-b.json`, row `B7_drive_passes_no_reasons_to_the_envelope`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`

Old text:

```
                permanent_reasons=_permanent_reasons_of(result.job.cause).get(
                    PERMANENT_REASONS, ()
                )
                if result.job.cause is not None
                else (),
```

New text:

```
                permanent_reasons=(),
```

### `r704-a.E2_job_verdict_needs_every_item_retryable`

existing guard sample: the job verdict is transient only when every failure is, so a mixed job reads permanent

- File: `src/cratekit/core/jobs_drive.py`
- Source: `r704-a.json`, row `E2_job_verdict_needs_every_item_retryable`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_failures_include_a_retryable_cause_stays_retryable`

Old text:

```
    if not failed or any(cause.retryable for cause in failed):
```

New text:

```
    if not failed or all(cause.retryable for cause in failed):
```

### `u169.E1_declined_accepts_retryable`

Declined: drop the refusal of a retryable cause, so a transient failure can be skipped and never retried

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E1_declined_accepts_retryable`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_handler_that_declines_a_retryable_cause_fails_the_item_rather_than_skipping_it`
  - `tests/test_jobs.py::test_a_retryable_cause_cannot_decline_an_item`

Old text:

```
        if cause.retryable:
            raise ValueError(
```

New text:

```
        if False:
            raise ValueError(
```

### `u169.E2_drive_fails_a_decline`

drive: no Declined clause, so a declined item falls to the failure boundary and fails the job

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E2_drive_fails_a_decline`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_job_every_item_of_which_was_declined_succeeds_rather_than_failing`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
                except Declined as exc:
```

New text:

```
                except Parked as exc:
```

### `u169.E3_decline_writes_failed`

decline_item: record the item failed rather than skipped

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E3_decline_writes_failed`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.FAILED), json.dumps(cause.to_json()), job_id, item_id),
```

### `u169.E4_decline_drops_cause`

decline_item: keep no cause on the skipped item, so nothing can name why

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E4_decline_drops_cause`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.SKIPPED), None, job_id, item_id),
```

### `u169.E6_failed_cause_hides_declines`

partial failure cause: say nothing of the declined items beside the failures

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E6_failed_cause_hides_declines`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`

Old text:

```
    if result.declined:
```

New text:

```
    if False:
```

### `u270.J3_park_releases_the_batch`

drive: ignore a Parked among a batch's outcomes, so the batch is settled as failed and the next batch is the second request into a block

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J3_park_releases_the_batch`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_park_answered_for_one_item_releases_the_whole_batch`
  - `tests/test_jobs_batch.py::test_a_park_raised_by_the_batch_releases_it_whole_and_blocks_the_job`
  - `tests/test_jobs_batch.py::test_a_parked_batch_is_driven_again_from_its_first_item`

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

### `u270.J4_signal_releases_the_batch`

drive: commit a batch answered under a signal, so a stop part way settles what the handler cut short

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J4_signal_releases_the_batch`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`

Old text:

```
                    return result
                if interrupt.signalled:
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break
                for item in claimed:
```

New text:

```
                    return result
                for item in claimed:
```

### `u270.J5_declined_outcome`

drive: settle a declined outcome as failed, so a batch item the worker declined fails the job

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J5_declined_outcome`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_each_outcome_settles_its_own_item`

Old text:

```
                    if isinstance(outcome, Declined):
```

New text:

```
                    if False:
```

### `u270.J6_missing_outcome_fails`

_batch_outcomes: read an item the handler gave no outcome for as done

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J6_missing_outcome_fails`
- Moved: _batch_outcomes moved whole from core/jobs.py to core/jobs_drive.py with the drive loop (U301); the test that killed it, test_an_item_the_handler_answered_nothing_for_is_failed_not_done, is now the no-answer case of test_an_item_without_a_usable_outcome_is_failed_not_done in the same file, the same input and the same check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_an_item_without_a_usable_outcome_is_failed_not_done[no-answer]`

Old text:

```
            outcomes[item.item_id] = _no_outcome(item)
```

New text:

```
            outcomes[item.item_id] = None
```

### `u270.J7_raise_is_every_outcome`

_batch_outcomes: a raise out of the batch handler fails only the first item, and the rest have no outcome

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J7_raise_is_every_outcome`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_that_fails_every_item_records_the_job_failed_then_raises`
  - `tests/test_jobs_batch.py::test_a_raise_out_of_the_batch_handler_is_every_items_outcome`

Old text:

```
        return {item.item_id: exc for item in claimed}
```

New text:

```
        return {claimed[0].item_id: exc}
```

### `u270.J8_stop_is_the_signal`

drive: hand the batch handler a stop that never answers true, so a signal waits for a whole batch's matching

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J8_stop_is_the_signal`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_a_batch_answered_under_a_signal_is_released_whole_and_the_job_cancelled`

Old text:

```
                    batch, job, claimed, lambda: interrupt.signalled
```

New text:

```
                    batch, job, claimed, lambda: False
```

### `u270.J9_outcome_type_check`

_batch_outcomes: pass an outcome that is neither produced nor an exception through to the commit

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u270.json`, row `J9_outcome_type_check`
- Moved: _batch_outcomes moved whole from core/jobs.py to core/jobs_drive.py with the drive loop (U301); the test that killed it, test_an_outcome_that_is_neither_produced_nor_an_exception_fails_its_item, is now the neither-produced-nor-an-exception case of test_an_item_without_a_usable_outcome_is_failed_not_done in the same file, now also asserting the message
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs_batch.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs_batch.py::test_an_item_without_a_usable_outcome_is_failed_not_done[neither-produced-nor-an-exception]`

Old text:

```
        if outcome is not None and not isinstance(outcome, (Produced, Exception)):
```

New text:

```
        if False:
```

### `r83-round-2.I1_fold_case`

R-344, after fix round 1: normalize_identity strips but no longer folds the case

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I1_fold_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`

Old text:

```
    return identity.strip().lower()
```

New text:

```
    return identity.strip()
```

### `r83-round-2.I3_configured_compare_exact`

R-344, after fix round 1: the configured mount's compare goes back to exact equality

- File: `src/cratekit/core/preflight.py`
- Source: `r83-round-2.json`, row `I3_configured_compare_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_identity_typed_as_diskutil_prints_it_passes_the_mount_check`

Old text:

```
    if same_identity(recorded_identity, observed):
```

New text:

```
    if observed == recorded_identity:
```

### `u27-round-8-independent.E4_path_missing_reads_ok`

A matching identity with an absent root resolves to OK instead of LIBRARY_PATH_MISSING

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E4_path_missing_reads_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unresolved_session_is_never_reported_clean_because_its_disk_is_gone`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`

Old text:

```
            MountState.OK if root_exists else MountState.LIBRARY_PATH_MISSING,
```

New text:

```
            MountState.OK,
```

### `u27-round-8-independent.E5_unmounted_reads_foreign`

An absent volume resolves to FOREIGN_VOLUME instead of NOT_MOUNTED

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E5_unmounted_reads_foreign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_unmounted_volume_and_a_moved_volume_produce_different_messages`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_write_when_the_volume_is_not_mounted_at_all`

Old text:

```
        MountState.NOT_MOUNTED if not root_exists else MountState.FOREIGN_VOLUME,
```

New text:

```
        MountState.FOREIGN_VOLUME,
```

### `u27-round-8-independent.E6_write_table_shares_read`

Make the write table refuse LIBRARY_PATH_MISSING, the row it differs from the read table on

- File: `src/cratekit/core/preflight.py`
- Source: `u27-round-8-independent.json`, row `E6_write_table_shares_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_renamed_library_folder_on_the_right_volume_is_written_not_refused`
  - `tests/test_doctor.py::test_every_mount_outcome_permits_exactly_what_it_is_declared_to[_STATE_WRITABLE-expected1]`
  - `tests/test_doctor.py::test_the_two_tables_differ_in_three_rows_and_every_one_is_a_read_signal_removed`

Old text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.ALWAYS,
```

New text:

```
    MountState.LIBRARY_PATH_MISSING: Reach.NEVER,
```

### `u329.P1_rb_changes_wrong_family`

rb_changes binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_changes.py`
- Source: `u329.json`, row `P1_rb_changes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 18 (killed)
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
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET BPM = 12400 WHERE ID = :id-BPM]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[UPDATE djmdContent SET KeyID = '283157525' WHERE ID = :id-KeyID]`
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_landed_rows_carry_what_rekordbox_loads_and_no_analysis_value`
  - ... and 3 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `r1665.W1_check_opens_the_capture`

integrity_ok: open the file it is given rather than its throwaway copy, the defect itself

- File: `src/cratekit/core/rb_copies.py`
- Source: `r1665.json`, row `W1_check_opens_the_capture`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_copies.py, the same guard in integrity_ok, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 12 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_base_drive_not_the_mount_rehearses_equal`
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[no room]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_gridless-a landed row carries an analysis value]`
  - `tests/test_intake_land_rehearse.py::test_a_landed_row_the_read_back_refuses_is_refused[assert_rows_identified-a landed row has no file id]`
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_folder_holds_is_refused_at_the_area`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_another_runs_area_alone`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_leaves_staging_music_and_database_as_they_were`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`
  - `tests/test_intake_land_rehearse.py::test_on_a_drive_recorded_as_its_mount_it_is_as_it_was`

Old text:

```
                db = _writer().open_db(checked, check_app_version=False, unlock=unlock)
```

New text:

```
                db = _writer().open_db(snapshot_database, check_app_version=False, unlock=unlock)
```

### `u329.P2_rb_copies_wrong_family`

rb_copies binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_copies.py`
- Source: `u329.json`, row `P2_rb_copies_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 20 (killed)
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
  - ... and 5 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `r1890.P5_gate_name_in_rb_nodes`

rb_nodes, a part, names the cloud sync gate and its flag, the command vocabulary the core may not learn

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r1890.json`, row `P5_gate_name_in_rb_nodes`
- Moved: U329 replaced rb_nodes' own _writer definition with the import of the shared accessor from rb_call_time; the same gate name is planted after that import, the guard it tests unchanged
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_core_writer_never_learns_the_gates_name_or_any_flag_string`

Old text:

```
from cratekit.core.rb_call_time import writer as _writer

```

New text:

```
from cratekit.core.rb_call_time import writer as _writer

_GATE = ("write.cloudsync.unreadable", "--decision")

```

### `r235-b.M22_nested_namesake_is_a_root`

a folder of the tree's name anywhere in the library is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M22_nested_namesake_is_a_root`
- Moved: U953 inlined _is_folder into is_folder, so the condition now reads is_folder; dropping its parent clause is the same unbounded root
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_namesake_nested_under_another_folder_is_not_a_root`
  - `tests/test_cutover_cli.py::test_a_nested_namesake_alone_is_no_root_at_all`

Old text:

```
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if is_folder(playlist)
```

### `r235-b.M23_playlist_is_a_root`

a playlist of the tree's name under the playlist root is a candidate root

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r235-b.json`, row `M23_playlist_is_a_root`
- Moved: U953 inlined _is_folder into is_folder, so the condition now reads is_folder; dropping that folder clause is the same playlist taken as a root
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_playlist_of_the_trees_name_is_not_a_root`

Old text:

```
        if is_folder(playlist)
        and str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

New text:

```
        if str(getattr(playlist, "ParentID", "")) in ROOT_PARENT_SENTINELS
```

### `u111-a.A1_folder_refused`

The writer no longer refuses a folder or smart playlist as the node it moves or removes

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A1_folder_refused`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_folder_a_parent_not_a_folder_and_a_removed_playlist`

Old text:

```
    if int(getattr(playlist, "Attribute", -1)) != 0:
        raise _node_refusal(
```

New text:

```
    if False:
        raise _node_refusal(
```

### `u111-a.A3_parent_not_folder`

move_playlist_node no longer refuses a parent that is not a live folder

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A3_parent_not_folder`
- Moved: U953 inlined _is_folder into is_folder, so the parent check of move_playlist_node now reads is_folder and disabling it is the same dropped refusal
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_writer_refuses_a_folder_a_parent_not_a_folder_and_a_removed_playlist`

Old text:

```
    if not is_folder(parent) or _writer().node_removed(parent):
```

New text:

```
    if False:
```

### `u111-a.A4_memberships_unmarked`

remove_playlist_node marks the node and leaves its own memberships live

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A4_memberships_unmarked`
- Moved: U953 replaced the local rb_writer name with a _writer() call on the marking line that follows, so skipping the membership marking is the same defect at the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    marked = _writer().remove_memberships(db, playlist, held)
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
```

New text:

```
    marked = list(held)
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
```

### `u111-a.A5_node_unmarked`

remove_playlist_node marks the memberships and never the node itself

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A5_node_unmarked`
- Moved: U953 replaced the local rb_writer name with a _writer() call, so deleting this setattr is the same node left unmarked
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
    setattr(playlist, _writer().SOFT_DELETE_COLUMN, 1)
    playlist.updated_at = datetime.now()
    return marked
```

New text:

```
    playlist.updated_at = datetime.now()
    return marked
```

### `u111-a.A7_content_compared`

The node judge no longer compares the content table

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-a.json`, row `A7_content_compared`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after0-djmdContent]`

Old text:

```
    if before.content != after.content:
        changed = sorted(
```

New text:

```
    if False:
        changed = sorted(
```

### `u111-b.A10_renumber_scoped`

The node judge admits a position change in any parent, not only one a node left or joined

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A10_renumber_scoped`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`

Old text:

```
        elif str(old[parent_at]) in renumbered:
            allowed = _SIBLING_COLUMNS
        else:
            allowed = frozenset()
```

New text:

```
        else:
            allowed = _SIBLING_COLUMNS
```

### `u111-b.A12_removed_keeps_no_live`

The node judge no longer asks that a removed node keeps no live membership

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A12_removed_keeps_no_live`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after3-is still live]`

Old text:

```
        if str(row[owner_at]) in gone and not row[m_marker]:
```

New text:

```
        if False:
```

### `u111-b.A13_confinement_raises`

assert_node_changes_confined computes the violations and never raises

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A13_confinement_raises`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`

Old text:

```
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if violations:
        db.rollback()
```

New text:

```
    violations = node_change_violations(
        before, after, moved=moved, removed=removed, created=created
    )
    if False:
        db.rollback()
```

### `u111-b.A8_membership_owner`

The node judge admits a changed membership in any playlist, not only a removed one

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A8_membership_owner`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after1-only a removed playlist]`

Old text:

```
        owner = str(old[owner_at])
        if owner not in gone:
```

New text:

```
        owner = str(old[owner_at])
        if False:
```

### `u111-b.A9_planned_move_made`

The node judge no longer asks whether each planned move sits live under its folder

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u111-b.json`, row `A9_planned_move_made`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after5-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after6-not live under the planned]`

Old text:

```
        if new is None or str(new[parent_at]) != planned_moves[key] or new[marker_at]:
```

New text:

```
        if new is None:
```

### `u127.W1_writable_always`

The writer's question always answers writable

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u127.json`, row `W1_writable_always`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return False
```

New text:

```
        if exc.cause.reason != "mytag-category-template-missing":
            raise
        return True
```

### `u127.W2_writable_reason_drift`

The writer's question reads another reason than the writer raises

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u127.json`, row `W2_writable_reason_drift`
- Moved: the same text, now in src/cratekit/core/rb_nodes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_vox_native.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`

Old text:

```
        if exc.cause.reason != "mytag-category-template-missing":
```

New text:

```
        if exc.cause.reason != "mytag-category-missing":
```

### `u329.P3_rb_nodes_wrong_family`

rb_nodes binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u329.json`, row `P3_rb_nodes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 17 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_removal_or_a_move_beyond_the_plan_is_refused_and_rolled_back`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`
  - `tests/test_inbox_rotate.py::test_the_judge_admits_exactly_the_planned_change_and_refuses_one_never_made_or_a_renumbering`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after0-djmdContent]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after1-only a removed playlist]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after10-rb_local_deleted]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after11-unplanned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after2-only its marker may go on]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after3-is still live]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after4-added or disappeared]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after5-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after6-not live under the planned]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after7-['Name']]`
  - `tests/test_inbox_rotate.py::test_the_judge_refuses_every_change_the_plan_does_not_explain[after8-does not carry the marker]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `u953.M11_is_folder_any_attribute`

is_folder reads any nonzero attribute as a folder, so a smart playlist is taken for one

- File: `src/cratekit/core/rb_nodes.py`
- Source: `u953.json`, row `M11_is_folder_any_attribute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_intake_land_labels_native.py`
- Collected: 73 against a baseline of 73
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`
  - `tests/test_intake_land_labels_native.py::test_a_tree_the_label_write_cannot_take_is_refused_before_the_gate`

Old text:

```
    return int(getattr(playlist, "Attribute", -1)) == 1
```

New text:

```
    return int(getattr(playlist, "Attribute", -1)) >= 1
```

### `r923.N19_default_is_an_analysis_column`

A tempo joins the defaults table, so the landing would declare an analysis column

- File: `src/cratekit/core/rb_tables.py`
- Source: `r923.json`, row `N19_default_is_an_analysis_column`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 93 against a baseline of 93
- Kills: 31 (killed)
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
  - `tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - ... and 16 more, see the JSON sidecar

Old text:

```
        "Rating": 0,
        "ColorID": "0",
```

New text:

```
        "Rating": 0,
        "BPM": 0,
        "ColorID": "0",
```

### `u111-a.A6_playlist_not_removable`

REMOVABLE_TABLES loses the playlist table, so the rotation's commit cannot carry a removed node

- File: `src/cratekit/core/rb_tables.py`
- Source: `u111-a.json`, row `A6_playlist_not_removable`
- Moved: the same text, now in src/cratekit/core/rb_tables.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_commit_naming_the_rotation_tables_admits_a_node_marker_and_no_content_marker`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_a_second_run_plans_nothing_and_still_asks_and_old_is_reused`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_one_hundred_twenty_goes_no_track_moves_then_two_stages`

Old text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE, PLAYLIST_TABLE})
```

New text:

```
REMOVABLE_TABLES = frozenset({MEMBERSHIP_TABLE})
```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 8 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = True

```

### `r239-a.A4_open_default_true`

open_db's unlock default back to True, so the probe branch never fires for an unnamed open

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A4_open_default_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 8 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`

Old text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = None,

```

New text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = True,

```

### `r239-a.A7_needed_always_true`

unlock_needed answers encrypted for every readable file, the U55 row that read zero with no encrypted input

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A7_needed_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 8 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return True
```

### `r239-a.A9_header_nearby_value`

The plain header constant to a realistic nearby value, SQLite format 4, so no plain file matches it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A9_header_nearby_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 8 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`

Old text:

```
SQLITE_HEADER = b"SQLite format 3"
```

New text:

```
SQLITE_HEADER = b"SQLite format 4"
```

### `r746-a.G4_read_back_walks_session_new_only`

assert_created_rows_are_gridless: the R-760 blind spot put back, a flushed creation is never read from SQL

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G4_read_back_walks_session_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`

Old text:

```
    instances = {**_registry_created_instances(db), **pending}
```

New text:

```
    instances = {**pending}
```

### `r746-a.G6_analysis_tables_not_checked`

assert_created_rows_are_gridless: no cue, mixer or file row is looked for on the new content row

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G6_analysis_tables_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit[sql2-djmdMixerParam]`

Old text:

```
        if table == CONTENT_TABLE and len(keys) == 1:
```

New text:

```
        if False:
```

### `r746-a.G7_sql_value_check_disarmed`

assert_created_rows_are_gridless: a value read from SQL is never a violation

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-a.json`, row `G7_sql_value_check_disarmed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if value not in EMPTY_ON_CREATE:
                violations.append(f"{table}.{name} = {value!r}")
```

New text:

```
            if False:
                violations.append(f"{table}.{name} = {value!r}")
```

### `r746-d.G5_content_row_read_back_against_five_not_ten`

assert_created_rows_are_gridless: a content row is held to the playlist tables' five columns, so a key or a rate rides in. Measured again after the key taint test its zero bought

- File: `src/cratekit/core/rb_writer.py`
- Source: `r746-d.json`, row `G5_content_row_read_back_against_five_not_ten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        policy = CONTENT_ROW_EMPTY_COLUMNS if table == CONTENT_TABLE else GRIDLESS_ON_CREATE_COLUMNS
```

New text:

```
        policy = GRIDLESS_ON_CREATE_COLUMNS
```

### `u185.G1_commit_guard_called`

commit_guarded: drop the foreign folder guard from the commit

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G1_commit_guard_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 13 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[folder-renamed]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[position-named-at-the-top]`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
            assert_created_rows_are_gridless(db)
            assert_foreign_untouched(db)
```

New text:

```
            assert_created_rows_are_gridless(db)
```

### `u185.G2_unread_refuses`

assert_foreign_untouched: a handle with no reading at open reads the subtree now and goes on

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G2_unread_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`

Old text:

```
    before = foreign_tree.reading_at_open(db)
    if before is None:
```

New text:

```
    before = foreign_tree.reading_at_open(db) or foreign_tree.read(db.session)
    if before is None:
```

### `u185.G3_pending_leg`

assert_foreign_untouched: drop the pending object leg, keep the second reading

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G3_pending_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 7 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[folder-renamed]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`

Old text:

```
    violations = foreign_tree.pending_touches(pending_objects(session, db), before)
```

New text:

```
    violations = []
```

### `u185.G4_second_reading_leg`

assert_foreign_untouched: drop the second reading from SQL, keep the pending objects

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G4_second_reading_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
    violations += foreign_tree.differences(before, foreign_tree.read(session))
```

New text:

```
    violations += []
```

### `u185.G5_reading_at_open`

open_db: keep no reading of the subtree as the handle opens

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G5_reading_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 12 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_a_pushed_playlist_moved_out_of_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_write_beside_the_folder_commits_and_leaves_every_row_the_push_wrote`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-added]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[membership-rewritten-to-another-owner]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[playlist-made-inside]`
  - `tests/test_foreign_tree.py::test_a_write_to_the_push_is_refused_and_rolled_back[position-named-at-the-top]`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`
  - `tests/test_foreign_tree.py::test_the_reading_at_open_names_the_push_and_not_a_namesake_below_the_top`

Old text:

```
    foreign_tree.remember(db)
    return db
```

New text:

```
    return db
```

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`
- Collected: 463 against a baseline of 463
- Kills: 158 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - `tests/test_deletion.py::test_a_confirmed_item_invalidated_before_the_move_is_refused_at_move_time`
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_corrected_prefix_rule_lets_the_confirmed_deletion_through_on_the_retry`
  - `tests/test_deletion.py::test_a_dead_prefix_rule_stops_the_whole_pass_before_anything_is_offered`
  - `tests/test_deletion.py::test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move`
  - `tests/test_deletion.py::test_a_different_disk_at_a_mapped_target_stops_the_apply_before_any_file_moves`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_stops_a_confirmed_move`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_featured_credit_bracket_does_not_stand_in_for_the_remix`
  - ... and 143 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `r1890.P9_sidecar_suffix_typed_in_restore_perform`

restore_perform, a part, types a SQLite companion suffix instead of reading which sidecars come back from the declaration

- File: `src/cratekit/core/restore_perform.py`
- Source: `r1890.json`, row `P9_sidecar_suffix_typed_in_restore_perform`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_restore_unit_derives_its_target_set_rather_than_listing_it`

Old text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore

```

New text:

```
def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


_COMPANION = "master.db-wal"

```

### `r815-a.W4_the_next_ordinal_is_past_the_floor`

_NEXT_ORDINAL: allocate one past the highest item alone, as before

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W4_the_next_ordinal_is_past_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_ordinal_a_withheld_item_held_is_never_given_to_a_later_one`
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
    "(SELECT MAX(COALESCE((SELECT MAX(ordinal) FROM review_items), 0), "
    "COALESCE((SELECT MAX(ordinal) FROM ordinal_floor), 0)) + 1)"
```

New text:

```
    "(SELECT COALESCE((SELECT MAX(ordinal) FROM review_items), 0) + 1)"
```

### `r815-a.W6_redescribe_only_an_open_item`

redescribe: rewrite an item whatever its verdict column says

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W6_redescribe_only_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_redescribing_a_decided_item_changes_nothing`
  - `tests/test_label_judge.py::test_redescribing_an_item_with_an_unreadable_verdict_changes_nothing`

Old text:

```
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ? AND verdict IS NULL",
```

New text:

```
            "UPDATE review_items SET payload = ?, updated = ? "
            "WHERE item_id = ?",
```

### `r840-c.C1_the_function_is_handed_the_payload_as_it_stands`

review.redescribe: hand the function an empty payload and not the stored one, so a caller changing one field writes that field alone

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C1_the_function_is_handed_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_person_reads_each_release_without_asking_for_json`
  - `tests/test_label_artists.py::test_a_rewrite_given_a_function_is_handed_the_payload_and_writes_what_it_returns`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_imported_item_is_read_by_the_identifier_its_payload_carries`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_label_marked_any_has_nothing_held_and_nobody_is_asked`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            wanted = payload(_payload_of(held["payload"]))
```

New text:

```
            wanted = payload({})
```

### `r840-c.C2_the_function_is_only_handed_an_open_item`

review.redescribe: read the payload of any item, so the function is called for one that is decided or carries a verdict this build cannot read

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C2_the_function_is_only_handed_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`
- Collected: 61 against a baseline of 61
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[accepted]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[rejected]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_an_item_with_an_unreadable_verdict`

Old text:

```
                "SELECT payload FROM review_items WHERE item_id = ? AND verdict IS NULL",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

New text:

```
                "SELECT payload FROM review_items WHERE item_id = ?",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

### `r790-d.R1_grouping_kinds`

grouped: count every kind in the queue, harvested label names included

- File: `src/cratekit/core/review_groups.py`
- Source: `r790-d.json`, row `R1_grouping_kinds`
- Moved: the same text, now in src/cratekit/core/review_groups.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_harvested_label_name_is_not_counted_as_a_label_release`

Old text:

```
    kinds = kinds or GROUPED_KINDS.get(declared)
```

New text:

```
    kinds = kinds
```

### `r790-d.R2_label_beyond`

grouped by label: report no recorded beyond

- File: `src/cratekit/core/review_groups.py`
- Source: `r790-d.json`, row `R2_label_beyond`
- Moved: the same text, now in src/cratekit/core/review_groups.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`
- Collected: 39 against a baseline of 39
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                "beyond": latest[key].beyond if key in latest else None,
```

New text:

```
                "beyond": None,
```

### `r798-c.H2_only_a_hold_in_force_is_dropped`

review.release_hold: drop a hold in any state, so the record that a person returned a release is lost and it can be held again

- File: `src/cratekit/core/review_holds.py`
- Source: `r798-c.json`, row `H2_only_a_hold_in_force_is_dropped`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_releasing_drops_a_hold_in_force_and_keeps_a_returned_one`

Old text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ? AND state = ?",
            (_assert_declared_queue(queue), item_id, HOLD_HELD),
```

New text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ?",
            (_assert_declared_queue(queue), item_id),
```

### `r815-a.W1_withhold_only_an_open_item`

withhold: move an item whatever its verdict column says

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W1_withhold_only_an_open_item`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was[accepted]`
  - `tests/test_label_judge.py::test_a_decided_item_is_not_withheld_and_stays_exactly_as_it_was[rejected]`
  - `tests/test_label_judge.py::test_a_release_decided_while_it_was_being_judged_is_not_held`
  - `tests/test_label_judge.py::test_a_superseded_item_is_not_withheld`
  - `tests/test_label_judge.py::test_an_item_carrying_a_verdict_this_build_cannot_read_is_not_withheld`

Old text:

```
        if row is None or row["verdict"] is not None:
            return None
        queue = row["queue"]
```

New text:

```
        if row is None:
            return None
        queue = row["queue"]
```

### `r815-a.W2_a_returned_hold_is_not_withheld`

withhold: take back a release a person returned

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W2_a_returned_hold_is_not_withheld`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_a_person_returned_is_never_withheld_again`

Old text:

```
        if standing is not None and standing["state"] == HOLD_RETURNED:
            return None
        try:
```

New text:

```
        if False:
            return None
        try:
```

### `r815-a.W3_the_floor_is_never_lowered`

withhold: let a lower ordinal replace the floor

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W3_the_floor_is_never_lowered`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
"ON CONFLICT(id) DO UPDATE SET ordinal = MAX(ordinal, excluded.ordinal)",
```

New text:

```
"ON CONFLICT(id) DO UPDATE SET ordinal = excluded.ordinal",
```

### `r815-a.W5_a_refresh_keeps_the_withheld_word`

_CARRIED_ACROSS_A_REFRESH: carry the filing run and drop the withheld word

- File: `src/cratekit/core/review_holds.py`
- Source: `r815-a.json`, row `W5_a_refresh_keeps_the_withheld_word`
- Moved: the same text, now in src/cratekit/core/review_holds.py, was in src/cratekit/core/review.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_refreshed_hold_keeps_the_run_its_release_was_filed_under`

Old text:

```
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD, WITHHELD_FIELD)
```

New text:

```
_CARRIED_ACROSS_A_REFRESH: tuple[str, ...] = (RUN_FIELD,)
```

### `r650-a.A1_tier_five_sets_nothing`

The last tier stops flagging its pass through, which is the state before this unit

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A1_tier_five_sets_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[unknown word]`
  - `tests/test_catalogue_searcher.py::test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline`
  - `tests/test_catalogue_searcher.py::test_the_resolver_fixtures_still_reach_the_tiers_they_name`

Old text:

```
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)
```

New text:

```
    return Suggestion(tag=value)
```

### `r650-a.A2_tier_five_flags_everything`

The last tier flags a bucket's own display, which routing places where the template says

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A2_tier_five_flags_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_the_correction_verb_cannot_write_a_genre_off_the_declared_taxonomy`

Old text:

```
    return Suggestion(tag=value, off_taxonomy=taxonomy.bucket_for_display(value) is None)
```

New text:

```
    return Suggestion(tag=value, off_taxonomy=True)
```

### `r650-a.A6_declared_literal_rule_flagged`

A declared rule carrying a literal tag and no bucket is reported as off taxonomy too

- File: `src/cratekit/core/routing.py`
- Source: `r650-a.json`, row `A6_declared_literal_rule_flagged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_searcher.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_searcher.py::test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown[declared tag with no bucket]`

Old text:

```
    return Suggestion(tag=rule.tag)
```

New text:

```
    return Suggestion(tag=rule.tag, off_taxonomy=True)
```

### `r798-a.K1_the_first_rule_that_matches_wins`

published_kind: read the published rules last first, so a word two rules could claim is given the later one's kind

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K1_the_first_rule_that_matches_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_published_word_is_matched_to_its_kind[first-rule-wins]`
  - `tests/test_label_genre_gate.py::test_a_published_word_is_matched_to_its_kind[long-rnb-is-not-the-blues-it-contains]`
  - `tests/test_label_genre_gate.py::test_every_measured_word_of_the_general_catalogue_is_a_kind`

Old text:

```
    for rule in taxonomy.label_gate.published:
```

New text:

```
    for rule in reversed(taxonomy.label_gate.published):
```

### `r798-a.K2_one_word_of_the_labels_kind_passes`

kind_verdict: pass only when every known word is the label's kind, so a crossover album listing a dance word beside a pop one is held

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K2_one_word_of_the_labels_kind_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_filed_release_says_the_gate_passed_it_and_on_which_words`
  - `tests/test_label_genre_gate.py::test_a_release_that_would_be_held_is_asked_about_again_before_it_is`
  - `tests/test_label_genre_gate.py::test_one_word_of_the_labels_kind_passes_a_release_listing_another_kind_too`

Old text:

```
    if any(found == judged_as for _word, found in placed):
```

New text:

```
    if placed and all(found == judged_as for _word, found in placed):
```

### `r798-a.K3_a_hold_needs_a_known_word`

kind_verdict: hold a release on words no rule knows, so absence of a verdict becomes a hold

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K3_a_hold_needs_a_known_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_word_no_rule_knows_is_not_judged_and_never_held`

Old text:

```
    if placed:
        others = ", ".join(dict.fromkeys(found for _word, found in placed))
```

New text:

```
    if words:
        others = ", ".join(dict.fromkeys(found for _word, found in placed))
```

### `r798-a.K4_a_label_of_any_kind_passes`

kind_settled: stop passing a label followed for any kind, so it is judged as a kind no rule names

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K4_a_label_of_any_kind_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_label_followed_for_any_kind_files_everything_and_asks_nothing`
  - `tests/test_label_genre_gate.py::test_a_label_followed_for_any_kind_passes_without_a_word`
  - `tests/test_label_genre_gate.py::test_a_label_of_any_kind_reads_no_track_and_asks_nothing`

Old text:

```
    if judged_as == ANY_KIND:
        return KindJudgment(
```

New text:

```
    if False:
        return KindJudgment(
```

### `r798-a.K5_a_kind_nothing_names_is_not_judged`

kind_settled: judge a label marked with a kind the taxonomy does not name, so every release of it with a known word is held

- File: `src/cratekit/core/routing.py`
- Source: `r798-a.json`, row `K5_a_kind_nothing_names_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_kind_the_taxonomy_does_not_name_is_not_judged_and_says_which`

Old text:

```
    if judged_as not in gate.kinds:
```

New text:

```
    if False:
```

### `r798-d.K11_the_shared_matcher_reads_a_substring_needle`

_rule_matches: drop the any_of arm of the matcher the second review made one function of, so no rule of either table that names a substring claims a word

- File: `src/cratekit/core/routing.py`
- Source: `r798-d.json`, row `K11_the_shared_matcher_reads_a_substring_needle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 58 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[African Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Alternative]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Asian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Blues]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Brazilian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Christian]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Classical]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Country]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Cumbia]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Dance]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Electro]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Films/Games]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Folk]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Indian Music]`
  - `tests/test_label_genre_gate.py::test_a_dance_label_passes_the_dance_words_and_holds_every_other[Jazz]`
  - ... and 43 more, see the JSON sidecar

Old text:

```
        or (rule.any_of and any(needle in value for needle in rule.any_of))
    )


def gate_decisions(
```

New text:

```
    )


def gate_decisions(
```

### `u155.R1_exact_match`

routing.genre_sub: match a source case insensitively, so rominimal reaches the sub

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R1_exact_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_only_the_exact_source_reaches_the_genre_sub[ROMINIMAL]`
  - `tests/test_genre_sub.py::test_only_the_exact_source_reaches_the_genre_sub[rominimal]`

Old text:

```
        if value in genre.sources:
```

New text:

```
        if value.lower() in {source.lower() for source in genre.sources}:
```

### `u155.R2_tagger_branch`

suggest_tag: answer a genre sub hit with the bucket's display, as before the unit

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R2_tagger_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[ROMINIMAL]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[Rominimal]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[rominimal]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_the_source_it_matched_when_a_sub_has_two`

Old text:

```
        genre = _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id)
        if genre is not None:
```

New text:

```
        genre = _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id)
        if False:
```

### `u155.R3_tagger_spelling`

suggest_tag: always write the first source, not the one the word matched

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R3_tagger_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_the_tagger_writes_the_source_it_matched_when_a_sub_has_two`

Old text:

```
            spelled = next(
                (source for source in genre.sources if source.lower().strip() == lowered),
                genre.sources[0],
            )
```

New text:

```
            spelled = genre.sources[0]
```

### `r118-a.A10_forget_uses_the_record_sentence`

A refusal from the remove half says the value is in the keychain because of this call, which is a claim about a write that never happened

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A10_forget_uses_the_record_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`

Old text:

```
    names = _index_read(REMOVE_NOTHING_TOUCHED)
```

New text:

```
    names = _index_read(RECORD_ALREADY_IN_THE_KEYCHAIN)
```

### `r118-a.A11_record_sentence_reworded`

The record sentence no longer says the value reached the keychain, only that the index could not be updated

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A11_record_sentence_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`

Old text:

```
    "THE VALUE IS IN THE KEYCHAIN. It was stored and read back before this index "
```

New text:

```
    "The index could not be updated. It was opened after the keychain write "
```

### `r118-a.A12_env_override_no_longer_short_circuits`

exists consults the index even when the opted-in environment fallback is supplying the value, so a machine that has no index by design is refused

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A12_env_override_no_longer_short_circuits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_the_environment_fallback_answers_presence_without_reading_the_index`

Old text:

```
    if _env_override(str(name)):
        return True
    return str(name) in _index_read()
```

New text:

```
    return str(name) in _index_read()
```

### `r118-a.A1_blanket_returns_empty`

The whole three-state reader reverts to the old blanket, so OSError and ValueError alike answer nothing recorded

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A1_blanket_returns_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 11 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_config.py::test_a_presence_index_without_a_list_of_names_refuses_rather_than_answering`
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`
  - `tests/test_config.py::test_recording_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_config.py::test_removing_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
    path = _index_path()
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
        raise refuse(
            "credential-index-unreadable",
            f"the credential presence index at {path} is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
            f"which credentials it has recorded. {left}",
            remedy=ProductRemedy.REPAIR_CREDENTIAL_STORE,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
        ) from exc
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise _damaged(
            path, f"is not readable as JSON ({type(exc).__name__})", left
        ) from exc
    names = payload.get("recorded") if isinstance(payload, dict) else None
    if not isinstance(names, Iterable) or isinstance(names, str):
        raise _damaged(path, "does not carry a list of recorded credential names", left)
    return frozenset(str(n) for n in names)
```

New text:

```
    del left
    path = _index_path()
    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError):
        return frozenset()
    names = payload.get("recorded") if isinstance(payload, dict) else None
    if not isinstance(names, Iterable) or isinstance(names, str):
        return frozenset()
    return frozenset(str(n) for n in names)
```

### `r118-a.A2_enoent_refuses_too`

A fresh installation with no index refuses instead of answering nothing recorded, so the product cannot be set up

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A2_enoent_refuses_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 34 (killed)
- Killed:
  - `tests/test_config.py::test_a_backend_that_accepts_a_write_and_stores_nothing_refuses`
  - `tests/test_config.py::test_a_backend_that_fails_with_an_unexpected_type_still_refuses_typed`
  - `tests/test_config.py::test_a_multi_field_credential_is_stored_as_one_blob`
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`
  - `tests/test_config.py::test_an_absent_presence_index_still_answers_nothing_recorded`
  - `tests/test_config.py::test_deleting_a_credential_clears_it_from_the_presence_index`
  - `tests/test_config.py::test_every_file_and_directory_this_unit_creates_is_private_under_any_umask`
  - `tests/test_config.py::test_presence_is_answered_without_retrieving_the_value`
  - `tests/test_config.py::test_recording_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_config.py::test_recording_and_reading_a_credential_round_trips`
  - `tests/test_config.py::test_removing_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_config.py::test_the_presence_index_cycle_is_held_under_an_exclusive_lock`
  - `tests/test_config.py::test_the_presence_index_records_names_and_never_values`
  - ... and 19 more, see the JSON sidecar

Old text:

```
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
```

New text:

```
    except OSError as exc:
```

### `r118-a.A3_unparseable_returns_empty`

Bytes that are not JSON answer nothing recorded again, the ValueError half of the old blanket

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A3_unparseable_returns_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`
  - `tests/test_doctor.py::test_the_wizard_notes_an_index_that_refuses_the_write_rather_than_dying`

Old text:

```
    except ValueError as exc:
        raise _damaged(
            path, f"is not readable as JSON ({type(exc).__name__})", left
        ) from exc
```

New text:

```
    except ValueError:
        return frozenset()
```

### `r118-a.A4_wrong_shape_returns_empty`

A payload whose recorded key is not a list of names answers nothing recorded

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A4_wrong_shape_returns_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_presence_index_without_a_list_of_names_refuses_rather_than_answering`

Old text:

```
    if not isinstance(names, Iterable) or isinstance(names, str):
        raise _damaged(path, "does not carry a list of recorded credential names", left)
```

New text:

```
    if not isinstance(names, Iterable) or isinstance(names, str):
        return frozenset()
```

### `r118-a.A5_refusal_drops_the_path`

The unreadable refusal names the exception type and not the file it could not read

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A5_refusal_drops_the_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
            f"the credential presence index at {path} is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
```

New text:

```
            f"the credential presence index is present and could not "
            f"be read ({type(exc).__name__}), so this installation cannot say "
```

### `r118-a.A6_refusal_not_raised_from`

The unreadable refusal is raised without from, so cause.classified cannot see the kernel's own refusal and a permission stays repair-credential-store

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A6_refusal_not_raised_from`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_presence_index_that_could_not_be_read_is_not_answered_as_not_recorded`
  - `tests/test_doctor.py::test_an_unreadable_credential_index_is_reported_as_unread_not_as_unrecorded`
  - `tests/test_doctor.py::test_the_wizard_notes_an_unreadable_credential_index_rather_than_dying`

Old text:

```
            detail={"path": str(path), "index": "unreadable"},
        ) from exc
```

New text:

```
            detail={"path": str(path), "index": "unreadable"},
        )
```

### `r118-a.A8_damaged_reports_as_unreadable`

Both states report index unreadable in detail, so a machine consumer cannot tell a file it could not open from one it read and could not use

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A8_damaged_reports_as_unreadable`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_damaged_presence_index_refuses_and_says_it_was_read`

Old text:

```
        detail={"path": str(path), "index": "damaged"},
```

New text:

```
        detail={"path": str(path), "index": "unreadable"},
```

### `r118-a.A9_record_uses_the_read_sentence`

A refusal from the record half says nothing was stored, over a value the keychain already holds

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A9_record_uses_the_read_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_record_half_says_the_value_reached_the_keychain`

Old text:

```
    names = _index_read(RECORD_ALREADY_IN_THE_KEYCHAIN)
```

New text:

```
    names = _index_read()
```

### `r118-b.D1_index_written_before_the_read_back`

set notes the name in the index before the keychain write is read back, so a null backend records a credential it discarded

- File: `src/cratekit/core/secrets.py`
- Source: `r118-b.json`, row `D1_index_written_before_the_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_backend_that_accepts_a_write_and_stores_nothing_refuses`

Old text:

```
        if stored != value:
            raise _unavailable(
```

New text:

```
        _record_name(str(name))
        if stored != value:
            raise _unavailable(
```

### `r118-b.D2_keychain_removed_before_the_index`

delete removes the keychain entry before the index entry, the order that made exists answer True for a credential that was gone

- File: `src/cratekit/core/secrets.py`
- Source: `r118-b.json`, row `D2_keychain_removed_before_the_index`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`
- Collected: 670 against a baseline of 670
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_a_refusal_from_the_remove_half_says_neither_store_was_touched`
  - `tests/test_config.py::test_deleting_a_credential_clears_it_from_the_presence_index`
  - `tests/test_config.py::test_removing_a_credential_does_not_truncate_an_index_it_could_not_read`
  - `tests/test_config.py::test_the_presence_index_cycle_is_held_under_an_exclusive_lock`
  - `tests/test_doctor.py::test_a_delete_that_fails_between_the_two_stores_never_reports_green`
  - `tests/test_doctor.py::test_recording_and_removing_still_work_when_the_lock_is_available`

Old text:

```
        _forget_name(str(name))
        try:
            keyring.delete_password(SERVICE, str(name))
```

New text:

```
        try:
            keyring.delete_password(SERVICE, str(name))
```

### `r118-c.A7_unreadable_remedy_is_set_credential`

The unreadable refusal carries set-credential, which is the advice the finding exists to stop

- File: `src/cratekit/core/secrets.py`
- Source: `r118-c.json`, row `A7_unreadable_remedy_is_set_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`

Old text:

```
            remedy=ProductRemedy.REPAIR_CREDENTIAL_STORE,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
```

New text:

```
            remedy=ProductRemedy.SET_CREDENTIAL,
            origin=("core", "secrets"),
            detail={"path": str(path), "index": "unreadable"},
```

### `r1255.S1_scan_unlisted_as_empty`

scan_log: answer a log it is refused as no record and none unread, the defect itself

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S1_scan_unlisted_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_inbox_unmirrored.py`
- Collected: 444 against a baseline of 444
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), (directory,)
```

New text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), ()
```

### `r1255.S2_absent_log_unread`

_listed: read a log that is not there as refused, so a library with no session refuses every write

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S2_absent_log_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`
- Collected: 467 against a baseline of 467
- Kills: 24 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_library_with_no_sessions_still_reports_a_clean_log`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_no_ok_detail_claims_a_volume_the_run_never_identified`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_strong_claim_survives_where_the_identity_really_was_compared`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_an_absent_session_log_is_no_record_at_all`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - ... and 9 more, see the JSON sidecar

Old text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        return None
```

New text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        raise
```

### `r1255.S7_log_unlisted_predicate`

log_unlisted: never name the unread half as the log, so every refusal counts it as one entry

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S7_log_unlisted_predicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
    return log_dir(cfg) in unreadable
```

New text:

```
    return False
```

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Moved: U953 folded this refusal's refuse call into the _defect builder, so the state test now guards raise _defect and disabling it is the same unguarded mark
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_only_a_run_waiting_on_an_import_has_one_to_verify`

Old text:

```
    if record.state is not SessionState.AWAITING_IMPORT:
        raise _defect(
```

New text:

```
    if False:
        raise _defect(
```

### `r501-a.S2_excusal_capture`

session.owes_only_deferred_routing: drop the no capture condition, so a run holding a capture is excused from the cutover precheck

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S2_excusal_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[holding-a-capture]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.S3_excusal_proof`

session.owes_only_deferred_routing: drop the proof condition, so any open run with no capture is excused, a crashed landing included

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S3_excusal_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_intake_imported.py`
- Collected: 60 against a baseline of 60
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress`
  - `tests/test_intake_imported.py::test_the_precheck_refuses_an_open_run_with_no_proof_recorded`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
```

### `r501-a.S4_excusal_state`

session.owes_only_deferred_routing: drop the open state condition, so a committed-unverified run carrying the key is excused

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S4_excusal_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[not-open]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r598-a.A5_holder_never_recorded`

open_session: drop the holder instead of recording it, so no record is ever provably orphaned and a hard kill is a dead end again

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A5_holder_never_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`

Old text:

```
        detail={HOLDER_KEY: holder.to_json()} if holder is not None else {},
```

New text:

```
        detail={},
```

### `u331.S05_room_reexport_checks_nothing`

session.assert_room_for_check: the re-export the landing calls is replaced by a function that checks nothing, so a rehearsal's copy is made with no room measured

- File: `src/cratekit/core/session.py`
- Source: `u331.json`, row `S05_room_reexport_checks_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`

Old text:

```
from cratekit.core.snapshot import assert_room_for_check as assert_room_for_check

```

New text:

```

def assert_room_for_check(*_args, **_kwargs):
    return None


```

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
            "rule": self.rule,

```

New text:

```
(empty)
```

### `u138.S1_session_rule_gone`

A session's answer falls to the terminal check, as before U138

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if False:

```

### `u138.S2_any_answer_gets_the_age_rule`

Any recorded answer, a person's included, mints without a terminal on young backups

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`
- Collected: 1020 against a baseline of 1020
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if decided_by is not None:

```

### `u138.S8_rule_not_recorded`

The record always says the terminal rule minted it

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Moved: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`

Old text:

```
        shown=shown,
        rule=rule,

```

New text:

```
        shown=shown,
        rule=RULE_TERMINAL,

```

### `u329.P6_session_ack_wrong_family`

session_ack binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_ack.py`
- Source: `u329.json`, row `P6_session_ack_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`
- Collected: 82 against a baseline of 82
- Kills: 28 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_bucket_folder_that_does_not_exist_yet_is_not_mistaken_for_a_rename`
  - `tests/test_deferred_routing.py::test_a_crash_between_the_commit_and_the_mark_converges`
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_rekordbox_rename_refuses_rather_than_duplicating`
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_rename_converges_once_the_tree_layer_can`
  - `tests/test_deferred_routing.py::test_a_recovery_run_after_a_taxonomy_rename_converges_rather_than_duplicating`
  - `tests/test_deferred_routing.py::test_a_run_closes_once_the_routing_pass_has_placed_its_track`
  - `tests/test_deferred_routing.py::test_a_run_whose_export_was_never_imported_refuses_to_close`
  - `tests/test_deferred_routing.py::test_a_run_whose_track_has_not_been_imported_still_refuses_to_close`
  - `tests/test_deferred_routing.py::test_a_run_with_a_pending_track_refuses_to_close`
  - `tests/test_deferred_routing.py::test_a_run_with_nothing_to_route_closes`
  - `tests/test_deferred_routing.py::test_a_second_pass_over_a_settled_run_writes_nothing`
  - `tests/test_deferred_routing.py::test_a_second_run_deferring_one_file_does_not_take_over_the_first_runs_record`
  - `tests/test_deferred_routing.py::test_a_surfaced_track_closes_the_run_only_after_it_is_acknowledged`
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_deferred_routing.py::test_a_track_whose_membership_cannot_be_proved_is_not_marked`
  - ... and 13 more, see the JSON sidecar

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `u329.A2_session_accessor_returns_the_writer`

session_call_time.session returns rb_writer, not session, so the session parts read the writer's names

- File: `src/cratekit/core/session_call_time.py`
- Source: `u329.json`, row `A2_session_accessor_returns_the_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 96 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - `tests/test_deletion.py::test_a_confirmed_item_invalidated_before_the_move_is_refused_at_move_time`
  - `tests/test_deletion.py::test_a_confirmed_removal_the_person_deleted_in_the_finder_does_not_block_the_next_one`
  - `tests/test_deletion.py::test_a_corrected_prefix_rule_lets_the_confirmed_deletion_through_on_the_retry`
  - `tests/test_deletion.py::test_a_dead_prefix_rule_stops_the_whole_pass_before_anything_is_offered`
  - `tests/test_deletion.py::test_a_decline_recorded_between_the_plan_and_the_move_stops_the_move`
  - `tests/test_deletion.py::test_a_decline_the_queue_simply_does_not_hold_is_still_addressable`
  - `tests/test_deletion.py::test_a_decline_whose_review_item_cannot_be_addressed_refuses`
  - `tests/test_deletion.py::test_a_declined_row_holds_the_watermark_and_lets_it_go_when_revoked`
  - `tests/test_deletion.py::test_a_decoy_volume_at_the_configured_path_refuses_before_anything_resolves`
  - `tests/test_deletion.py::test_a_different_disk_at_a_mapped_target_stops_the_apply_before_any_file_moves`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - ... and 81 more, see the JSON sidecar

Old text:

```
    from cratekit.core import session

    return session
```

New text:

```
    from cratekit.core import rb_writer as session

    return session
```

### `r598-a.A3_liveness_not_consulted`

orphaned: skip holder_alive and judge every open record with a holder orphaned, so a running write's record is ended behind it

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-a.json`, row `A3_liveness_not_consulted`
- Moved: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`

Old text:

```
    return not holder_alive(holder, here=here)
```

New text:

```
    return True
```

### `u329.P7_session_holders_wrong_family`

session_holders binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_holders.py`
- Source: `u329.json`, row `P7_session_holders_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `r44-a.S2_proved_widened`

Let NOT_MOUNTED count as a proved identity, which is the pass set widening by one verdict

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S2_proved_widened`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`

Old text:

```
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)
```

New text:

```
    {
        preflight.MountState.OK,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.NOT_MOUNTED,
    }
)
```

### `r44-a.S4_inside_root_unheld`

Hold a rule inside the library root to nothing of the library's, so a nested foreign volume is judged as unrecorded rather than foreign

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S4_inside_root_unheld`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`

Old text:

```
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None
```

New text:

```
    return None
```

### `r44-a.S5_not_destructive`

Assert a rule target at read strength, where an unreadable or unrecorded identity is tolerated

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S5_not_destructive`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`

Old text:

```
                expected_rule_identity(cfg, rule),
                destructive=True,
```

New text:

```
                expected_rule_identity(cfg, rule),
                destructive=False,
```

### `r44-a.S7_probe_the_target`

Probe the rule's target for a file instead of the file's own directory, so a volume nested under the target is never seen

- File: `src/cratekit/core/session_volumes.py`
- Source: `r44-a.json`, row `S7_probe_the_target`
- Moved: the same text, now in src/cratekit/core/session_volumes.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`

Old text:

```
        rules[index],
        Path(path).parent,
```

New text:

```
        rules[index],
        Path(rules[index].target or "/"),
```

### `u329.P8_session_volumes_wrong_family`

session_volumes binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_volumes.py`
- Source: `u329.json`, row `P8_session_volumes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`
- Collected: 331 against a baseline of 331
- Kills: 7 (killed)
- Killed:
  - `tests/test_deletion.py::test_a_different_disk_at_a_mapped_target_stops_the_apply_before_any_file_moves`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_retires_nothing_nobody_answered_for`
  - `tests/test_deletion.py::test_a_disk_swapped_after_the_plan_stops_a_confirmed_move`
  - `tests/test_deletion.py::test_a_drive_ejected_mid_queue_is_not_settled_as_a_queue_of_deletions`
  - `tests/test_deletion.py::test_a_file_in_a_volume_nested_under_the_rules_target_is_not_moved`
  - `tests/test_deletion.py::test_a_rule_onto_the_wrong_volume_refuses_rather_than_trashing_the_only_copy`
  - `tests/test_deletion.py::test_a_volume_holding_only_removed_rows_does_not_settle_off_an_empty_mount_point`

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `r1677.C1_no_measure`

capture: never measure the throwaway's room, so a full temporary volume reads as a failed check again (the card's defect)

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C1_no_measure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`

Old text:

```
    if verifier is None:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

New text:

```
    if False:
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

### `r1677.C3_store_not_passed`

capture: measure the throwaway without the store, so a shared volume is asked for the throwaway alone

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `C3_store_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_no_room_for_the_check_refuses_before_its_copy`

Old text:

```
        assert_room_for_check(database_paths(cfg)[0], store=(destination_root, estimate))
```

New text:

```
        assert_room_for_check(database_paths(cfg)[0], store=None)
```

### `r1677.N1_every_failure_is_room`

check_had_no_room: read every copy failure as no room, so a permission error is told as a full volume

- File: `src/cratekit/core/snapshot.py`
- Source: `r1677.json`, row `N1_every_failure_is_room`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_failed_integrity_check_is_refused_naming_the_area[its copy otherwise]`

Old text:

```
    if code not in _NO_ROOM_ERRNOS:
        return None
```

New text:

```
    if False:
        return None
```

### `r432-b.B5_lock_on_the_library_volume`

config: declare the landing locks library scoped, which puts them on the volume that is commonly exFAT

- File: `src/cratekit/core/state_files.py`
- Source: `r432-b.json`, row `B5_lock_on_the_library_volume`
- Moved: the same entry's root: an installation entry is an _installation call now, so the mutation respells it as a never restored _library entry (U299)
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
    _installation(
        "landing_locks", "landing_locks",

```

New text:

```
    _library(
        "landing_locks", "landing_locks", SnapshotRole.NEVER_RESTORED,

```

### `r432-b.B6_lock_directory_renamed`

config: move the landing locks to another directory name under the state root

- File: `src/cratekit/core/state_files.py`
- Source: `r432-b.json`, row `B6_lock_directory_renamed`
- Moved: the same entry's relative path, now the second argument of its _installation call in state_files (U299)
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_landing.py::test_the_batch_lock_is_on_the_state_disk_and_a_released_one_leaves_its_file`

Old text:

```
        "landing_locks", "landing_locks",

```

New text:

```
        "landing_locks", "landings",

```

### `u278.M1_gate_follows_state`

state_path: drop the gate's own resolution, so the gate follows a redirected CRATEKIT_STATE_DIR and a copy gets a fresh hour

- File: `src/cratekit/core/state_files.py`
- Source: `u278.json`, row `M1_gate_follows_state`
- Moved: the same text, now in src/cratekit/core/state_files.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`

Old text:

```
        if key in _PROVIDER_GATE_KEYS:
            return provider_gate_dir() / entry.relative

```

New text:

```
(empty)
```

### `u299.U1_installation_never_restored`

_installation: an installation entry is captured with the library, coupled to a restore

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U1_installation_never_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_the_coupled_set_is_a_directory_boundary_rather_than_a_list`
  - `tests/test_config.py::test_the_locks_and_the_snapshot_store_are_not_in_the_coupled_set`
  - `tests/test_config.py::test_the_presence_index_lock_lives_beside_the_file_it_guards`

Old text:

```
        snapshot=SnapshotRole.NEVER_RESTORED,
        installation_area=area,
```

New text:

```
        snapshot=SnapshotRole.COUPLED,
        installation_area=area,
```

### `u299.U2_installation_area_passed`

_installation: the area an entry names is dropped, so config.toml resolves under the state directory

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U2_installation_area_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 417 against a baseline of 417
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_configuration_from_a_newer_build_keeps_its_own_remedy`
  - `tests/test_doctor.py::test_the_wizard_completes_an_incomplete_configuration_rather_than_refusing`
  - `tests/test_doctor.py::test_the_wizard_refuses_to_overwrite_a_configuration_it_cannot_understand`

Old text:

```
        installation_area=area,
    )
```

New text:

```
        installation_area=InstallationArea.STATE,
    )
```

### `u299.U3_installation_medium_passed`

_installation: every installation entry reads as a file, the keychain and directory entries included

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U3_installation_medium_passed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 5 (killed)
- Killed:
  - `tests/test_config.py::test_a_directory_entry_is_declared_a_directory_under_either_root[held_plans]`
  - `tests/test_config.py::test_a_directory_entry_is_declared_a_directory_under_either_root[job_queue]`
  - `tests/test_config.py::test_credentials_are_not_a_file_at_all`
  - `tests/test_config.py::test_every_installation_entry_resolves_under_a_directory_the_module_names`
  - `tests/test_config.py::test_no_two_state_entries_resolve_to_the_same_path`

Old text:

```
        root=StateRoot.INSTALLATION,
        medium=medium,
```

New text:

```
        root=StateRoot.INSTALLATION,
        medium=Medium.FILE,
```

### `u299.U4_library_root`

_library: a library entry is declared under the installation root

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U4_library_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 17 (killed)
- Killed:
  - `tests/test_config.py::test_a_previously_straddling_entry_is_two_files_with_distinct_names[label_crawl_cache-label_outcomes]`
  - `tests/test_config.py::test_a_previously_straddling_entry_is_two_files_with_distinct_names[label_intent-label_watermarks]`
  - `tests/test_config.py::test_a_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_config.py::test_config_carries_only_the_taxonomy_selection`
  - `tests/test_config.py::test_every_file_and_directory_this_unit_creates_is_private_under_any_umask`
  - `tests/test_config.py::test_every_installation_entry_resolves_under_a_directory_the_module_names`
  - `tests/test_config.py::test_no_two_state_entries_resolve_to_the_same_path`
  - `tests/test_config.py::test_resolving_a_library_scoped_entry_without_a_config_refuses`
  - `tests/test_config.py::test_the_capture_set_includes_the_databases_sqlite_sidecars`
  - `tests/test_config.py::test_the_locks_the_log_and_the_snapshots_live_with_the_library[favorites_state]`
  - `tests/test_config.py::test_the_locks_the_log_and_the_snapshots_live_with_the_library[session_lock]`
  - `tests/test_config.py::test_the_locks_the_log_and_the_snapshots_live_with_the_library[session_log]`
  - `tests/test_config.py::test_the_locks_the_log_and_the_snapshots_live_with_the_library[snapshots]`
  - `tests/test_config.py::test_the_locks_the_log_and_the_snapshots_live_with_the_library[write_lock]`
  - `tests/test_config.py::test_the_per_set_workspaces_resolve_from_configured_directory_names`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        root=StateRoot.LIBRARY,
        medium=medium,
```

New text:

```
        root=StateRoot.INSTALLATION,
        medium=medium,
```

### `u299.U5_library_snapshot_passed`

_library: the snapshot role an entry names is replaced by COUPLED for every library entry

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U5_library_snapshot_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 6 (killed)
- Killed:
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[energy_undo_log-never-restored]`
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[genre_tag_undo_log-never-restored]`
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[session_log-survives-rollback]`
  - `tests/test_config.py::test_each_named_entry_carries_its_declared_snapshot_role[snapshots-survives-rollback]`
  - `tests/test_config.py::test_the_locks_and_the_snapshot_store_are_not_in_the_coupled_set`
  - `tests/test_config.py::test_the_snapshot_store_does_not_nest_inside_what_it_snapshots`

Old text:

```
        why=why,
        snapshot=snapshot,
```

New text:

```
        why=why,
        snapshot=SnapshotRole.COUPLED,
```

### `u299.U7_library_extras_passed`

_library: the rollback effects, decision stores and sidecars an entry declares are dropped

- File: `src/cratekit/core/state_files.py`
- Source: `u299.json`, row `U7_library_extras_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_config.py::test_the_capture_set_includes_the_databases_sqlite_sidecars`
  - `tests/test_config.py::test_the_one_ported_shape_keyed_by_a_display_name_is_flagged_for_rekeying`
  - `tests/test_config.py::test_the_sidecars_are_declared_on_the_entry_rather_than_listed_by_a_consumer`

Old text:

```
        snapshot=snapshot,
        **extra,
    )
```

New text:

```
        snapshot=snapshot,
    )
```

### `r798-a.K6_the_default_kind_is_one_a_rule_names`

_build_gate: accept a default kind no published rule names, so every label left at the default is never judged

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r798-a.json`, row `K6_the_default_kind_is_one_a_rule_names`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_malformed_label_gate_is_refused_by_what_it_lacks[default-kind-no-rule-names]`

Old text:

```
    if published and default_kind != ANY_KIND and default_kind not in kinds:
```

New text:

```
    if False:
```

### `r798-a.K7_a_needle_is_folded_when_loaded`

_needles: keep a needle as it was typed, so one with a capital never matches a word that is matched lowercase

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r798-a.json`, row `K7_a_needle_is_folded_when_loaded`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_needle_typed_with_a_capital_still_matches`

Old text:

```
    return tuple(one.strip().lower() for one in raw), True
```

New text:

```
    return tuple(one.strip() for one in raw), True
```

### `r798-a.K8_a_kind_is_one_word`

_build_published: accept a rule naming a kind in a shape the registry refuses, so the taxonomy declares a kind no label can be given

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `r798-a.json`, row `K8_a_kind_is_one_word`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_malformed_label_gate_is_refused_by_what_it_lacks[rule-kind-of-two-words]`

Old text:

```
        if not KIND_NAME.fullmatch(kind):
```

New text:

```
        if False:
```

### `u111-d.F1_old_differs_from_intake`

The taxonomy accepts an [intake_old] that repeats the intake flow's id or display

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u111-d.json`, row `F1_old_differs_from_intake`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_an_old_folder_declared_wrongly_is_a_taxonomy_problem_and_not_a_traceback[declared1-must differ from [intake]]`
  - `tests/test_inbox_rotate.py::test_an_old_folder_declared_wrongly_is_a_taxonomy_problem_and_not_a_traceback[declared2-must differ from [intake]]`

Old text:

```
        if intake_old.id == intake.id or intake_old.display == intake.display:
```

New text:

```
        if False:
```

### `u155.T10_source_claimed`

_check_genre_subs: accept one source in two genre subs

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T10_source_claimed`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[one-source-in-two]`

Old text:

```
                if source in claimed:
```

New text:

```
                if False:
```

### `u155.T11_shape_check`

_build_buckets: read a genre_sub of the wrong shape as rows, not a problem

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T11_shape_check`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_in_the_wrong_shape_is_a_problem_and_not_a_crash[list-of-strings]`
  - `tests/test_genre_sub.py::test_a_genre_sub_in_the_wrong_shape_is_a_problem_and_not_a_crash[one-table]`
  - `tests/test_genre_sub.py::test_a_genre_sub_in_the_wrong_shape_is_a_problem_and_not_a_crash[string]`

Old text:

```
        if not isinstance(genre_raw, list) or not all(
            isinstance(row, Mapping) for row in genre_raw
        ):
```

New text:

```
        if False:
```

### `u155.T12_sources_type`

_sources: take any value as the sources, a bare string read letter by letter

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T12_sources_type`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[Rominimal]`
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[sources2]`

Old text:

```
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        return ()
    return tuple(raw)
```

New text:

```
    return tuple(raw or ())
```

### `u155.T13_live_places`

live_places: leave the genre subs out of the one list of what a folder holds

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T13_live_places`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_former_place_naming_the_genre_sub_is_refused_through_that_list`
  - `tests/test_genre_sub.py::test_live_places_names_the_genre_sub`

Old text:

```
    for genre in bucket.genre_subs:
        ids.add(genre.id)
        displays.add(genre.display)
    return ids, displays
```

New text:

```
    return ids, displays
```

### `u155.T14_tagging_index`

_build_alias_indexes: leave a genre sub's source tagging as the bucket's name

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T14_tagging_index`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[ROMINIMAL]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[Rominimal]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_rominimal_rather_than_the_buckets_name[rominimal]`
  - `tests/test_genre_sub.py::test_the_tagger_writes_the_source_it_matched_when_a_sub_has_two`

Old text:

```
                tagging[source.lower().strip()] = (bucket.id, genre.id)
```

New text:

```
                pass
```

### `u155.T1_version_guard`

_check_genre_subs: drop the schema version refusal, so a genre sub loads under version 4

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T1_version_guard`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_under_an_older_schema_version_is_refused_by_name[1]`
  - `tests/test_genre_sub.py::test_a_genre_sub_under_an_older_schema_version_is_refused_by_name[2]`
  - `tests/test_genre_sub.py::test_a_genre_sub_under_an_older_schema_version_is_refused_by_name[3]`
  - `tests/test_genre_sub.py::test_a_genre_sub_under_an_older_schema_version_is_refused_by_name[4]`

Old text:

```
        if version < GENRE_SUB_SCHEMA_VERSION:
```

New text:

```
        if False:
```

### `u155.T2_band_guard`

_check_genre_subs: drop the refusal of a genre sub on a bucket that does not split by energy

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T2_band_guard`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[bucket-routes-by-source]`
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[bucket-with-one-sub]`

Old text:

```
        if not _band_names(bucket, energy):
            problems.append(
                f"[[bucket]] {bucket.id}: declares a genre sub and does not split by "
```

New text:

```
        if False:
            problems.append(
                f"[[bucket]] {bucket.id}: declares a genre sub and does not split by "
```

### `u155.T3_id_pattern`

_check_genre_subs: accept any identifier, a display name included

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T3_id_pattern`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[identifier-not-one]`

Old text:

```
            if not _ID.match(genre.id):
                problems.append(f"{where}: id {genre.id!r} must match {_ID.pattern}")
            if not genre.display:
```

New text:

```
            if False:
                problems.append(f"{where}: id {genre.id!r} must match {_ID.pattern}")
            if not genre.display:
```

### `u155.T4_empty_display`

_check_genre_subs: accept an empty display, a playlist named the empty string

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T4_empty_display`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[empty-display]`

Old text:

```
            if not genre.display:
                problems.append(f"{where}: display must be a non-empty string")
            if genre.id in seen_ids:
```

New text:

```
            if False:
                problems.append(f"{where}: display must be a non-empty string")
            if genre.id in seen_ids:
```

### `u155.T5_duplicate_id`

_check_genre_subs: never record a seen genre sub id, so two of one id load

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T5_duplicate_id`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 1 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[two-of-one-identifier]`

Old text:

```
            seen_ids.add(genre.id)
```

New text:

```
            pass
```

### `u155.T6_id_collision`

_check_genre_subs: accept an id that is already a band, a sub or a sub class

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T6_id_collision`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[id-candy-id 'candy' is already a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[id-low-id 'low' is already a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[id-unsorted-id 'unsorted' is already a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[id-with_vox-id 'with_vox' is already a band]`

Old text:

```
            elif genre.id in taken_ids:
```

New text:

```
            elif False:
```

### `u155.T7_display_collision`

_check_genre_subs: accept a display that is already a band label, the no reading sub or a sub class

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T7_display_collision`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[display-Favorites-display 'Favorites' is already the name of a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[display-Low Energy-display 'Low Energy' is already the name of a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[display-Unsorted-display 'Unsorted' is already the name of a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_colliding_with_a_band_or_a_sub_class_is_refused_by_name[display-with vox-display 'with vox' is already the name of a band]`
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[two-of-one-name]`

Old text:

```
            if genre.display in taken_displays:
```

New text:

```
            if False:
```

### `u155.T8_empty_sources`

_check_genre_subs: accept a genre sub with no sources

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T8_empty_sources`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[None]`
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[Rominimal]`
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[sources0]`
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[sources2]`

Old text:

```
            if not genre.sources:
```

New text:

```
            if False:
```

### `u155.T9_source_alias`

_check_genre_subs: accept a source that is not an exact alias of the bucket

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T9_source_alias`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_sub.py`
- Collected: 48 against a baseline of 48
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[source-another-bucket-routes]`
  - `tests/test_genre_sub.py::test_a_genre_sub_that_is_not_a_place_of_its_own_is_refused_by_name[source-not-an-alias]`

Old text:

```
                if source not in aliases:
```

New text:

```
                if False:
```

