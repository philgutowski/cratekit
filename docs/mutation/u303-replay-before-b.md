# Mutation table: u303-replay-before-b

Measured by `scripts/mutate.py` on 2026-11-22 18:45 UTC, branch `HEAD` at `fd8173d3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 212.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 43, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/ce20fa78-0ba8-5393-bea1-e47f9b749a43/scratchpad/known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1334.E1_offer_after_compare` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 6 | killed |
| `r1334.E2_stale_compare_dropped` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 17 | killed |
| `r1334.E3_record_binds_no_offer` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 40 | killed |
| `r1334.S10_unknown_option_no_context` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 1 | killed |
| `r1334.S11_unknown_option_shown_dropped` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 1 | killed |
| `r1334.S1_stale_not_offered` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 10 | killed |
| `r1334.S2_stale_screen_without_plan` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 8 | killed |
| `r1334.S3_offered_ignored` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 10 | killed |
| `r1334.S4_screen_always` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 3 | killed |
| `r1334.S5_screen_no_shown` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 8 | killed |
| `r1334.S6_screen_shown_empty_for_none` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 1 | killed |
| `r1334.S7_screen_no_options` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 5 | killed |
| `r1334.S8_screen_no_prompt` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 1 | killed |
| `r1334.S9_screen_explicit_false` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1132 | 1 | killed |
| `r1349.C1_argv_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 5 | killed |
| `r1349.C2_run_dropped` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 5 | killed |
| `r1349.E2_open_left` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 10 | killed |
| `r1349.E3_offer_unrecorded` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 49 | killed |
| `r1349.N1_guard_gone` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 8 | killed |
| `r1349.N2_any_gate` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 2 | killed |
| `r1349.N3_offer_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 1 | killed |
| `r1349.N4_open_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 15 | killed |
| `r1349.N5_answered_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 1 | killed |
| `r1349.N6_offer_inverted` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 9 | killed |
| `r1349.N7_written_before_refusal` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 3 | killed |
| `r1349.N8_after_unknown_swapped` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 1 | killed |
| `r1349.R1_reason_open_gate` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 6 | killed |
| `r1349.R2_answer_remedy` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 2 | killed |
| `r1349.R3_waiting_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 3 | killed |
| `r1349.R4_continue_wrong` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 6 | killed |
| `r1349.R5_open_gate_detail` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 2 | killed |
| `r1349.R6_message_no_gate` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 2 | killed |
| `r1349.R7_answer_step_dropped` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1213 | 1 | killed |
| `u112.G1_part_unverified` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 215 | 1 | killed |
| `u161.G1_pin_never_compared` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 81 | 4 | killed |
| `u161.G2_pin_overwritten_before_compare` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 81 | 3 | killed |
| `u161.G3_absence_read_as_agreement` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 81 | 2 | killed |
| `u161.G4_pins_not_written` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 81 | 28 | killed |
| `u161.G5_pins_not_read` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 81 | 28 | killed |
| `u168.C12_argv_not_saved` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 1012 | 5 | killed |
| `u170.G1_threshold_boundary` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.G2_idle_from_start_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 3 | killed |
| `u170.G3_idle_from_write_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.G4_unstattable_is_old` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.G5_no_abort_retired` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 2 | killed |
| `u170.G6_missing_verb_branch` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.G8_malformed_stamp` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u183.M16_record_written_only_when_set` | `src/cratekit/cli/gates.py` | maintainer | 4 file(s) | 127 | 2 | killed |
| `u183.M17_record_read_back` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 86 | 7 | killed |
| `u183.M18_load_refuses_non_object` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 112 | 1 | killed |
| `u186.S10_scope_every_verb` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.S1_window_wider` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.S2_window_narrower` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S3_exclude_self` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 19 | killed |
| `u186.S4_other_verb` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S5_unreadable_dropped` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u186.S6_unrecorded_time_old` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S7_open_drops_answers` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.S8_open_read_as_answered` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 4 | killed |
| `u186.S9_unreadable_unsaid` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 34 | 2 | killed |
| `u211.D3_kept_set_is_narrow` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 229 | 1 | killed |
| `u49-author.G1_an_explicit_gate_takes_an_inline_answer_again` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.G2_the_second_raise_site_drops_the_context` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1987 | 1 | killed |
| `u270.H1_batch_size_floor` | `src/cratekit/cli/handlers.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u270.H2_run_job_drives_the_batch` | `src/cratekit/cli/handlers.py` | user | 4 file(s) | 290 | 7 | killed |
| `u274.H1_drive_not_entered` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 449 | 17 | killed |
| `u274.H2_warnings_dropped` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 449 | 3 | killed |
| `u46-author.H1_binding_removed` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 107 | 19 | killed |
| `u46-author.H2_is_known_always_true` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 107 | 3 | killed |
| `u46-author.H3_import_before_refusing` | `src/cratekit/cli/handlers.py` | maintainer | 3 file(s) | 107 | 1 | killed |
| `u46-author.H4_unbound_reason_silent` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 107 | 1 | killed |
| `u46-author.H5_fresh_config` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 107 | 2 | killed |
| `u46-author.H7_no_drift` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 107 | 2 | killed |
| `u46-author.H8_drift_wording_dropped` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 107 | 1 | killed |
| `u52-item-derivation.B1_label_import_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 314 | 6 | killed |
| `u52-item-derivation.B2_sync_labels_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 314 | 48 | killed |
| `u52-item-derivation.B3_sync_labels_wrong_worker` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 314 | 42 | killed |
| `u55-collection-reader.R30_scan_handler_bound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 286 | 9 | killed |
| `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 388 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 388 | 21 | killed |
| `u58-workers-and-wav.H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 8 file(s) | 642 | 33 | killed |
| `r290-author.S07_rebuild_call_removed` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 126 | 6 | killed |
| `u132.W5_rebuild_note` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u219.C1_rebuild_items_filtered` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u219.C2_rebuild_named_intake` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 5 | killed |
| `u219.K2_accept_actor` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u219.K3_accept_declined` | `src/cratekit/cli/rebuild.py` | user | 2 file(s) | 77 | 1 | killed |
| `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 21 | killed |
| `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.W4_rebuild_worker` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.W6_rebuild_resume_loads_first` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 3 | killed |
| `r1334.S12_render_no_stale_header` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1025 | 2 | killed |
| `r1334.S13_render_header_reworded` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1025 | 2 | killed |
| `r1334.S14_render_stale_offers_inline` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1025 | 1 | killed |
| `r1334.S15_render_open_gate_drops_inline` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1025 | 3 | killed |
| `r1334.S16_is_gate_screen_no_stale` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1025 | 2 | killed |
| `r1334.S17_is_gate_screen_any_stale` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1025 | 1 | killed |
| `r1334.S19_screen_test_drops_options_clause` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1010 | 1 | killed |
| `r378.G1_drop_the_review_set_case` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 3 | killed |
| `r378.G2_name_is_dumped_with_the_other_fields` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 2 | killed |
| `r378.G3_unresolved_is_omitted` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 4 | killed |
| `r378.G4_the_schema_gate_is_dropped` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 1 | killed |
| `r378.G5_items_are_printed_with_repr` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 3 | killed |
| `r378.G6_the_queue_is_omitted` | `src/cratekit/cli/render.py` | user | 1 file(s) | 82 | 2 | killed |
| `r395.M11_render_literal` | `src/cratekit/cli/render.py` | user | 7 file(s) | 2239 | 2 | killed |
| `r678-a.A10_proof_ungated_on_verb` | `src/cratekit/cli/render.py` | user | 2 file(s) | 102 | 1 | killed |
| `r678-a.A11_run_count_not_the_total` | `src/cratekit/cli/render.py` | user | 2 file(s) | 102 | 1 | killed |
| `r678-a.A12_retired_file_unnamed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 102 | 3 | killed |
| `r678-a.A1_drop_the_job_state_case` | `src/cratekit/cli/render.py` | user | 5 file(s) | 381 | 11 | killed |
| `r678-a.A2_drop_the_import_proof_case` | `src/cratekit/cli/render.py` | user | 2 file(s) | 102 | 2 | killed |
| `r678-a.A4_empty_job_id_renders_a_job` | `src/cratekit/cli/render.py` | user | 5 file(s) | 381 | 4 | killed |
| `r678-a.A5_drive_line_for_any_state` | `src/cratekit/cli/render.py` | user | 5 file(s) | 381 | 1 | killed |
| `r678-a.A6_resolution_for_every_job_verb` | `src/cratekit/cli/render.py` | user | 5 file(s) | 381 | 2 | killed |
| `r678-c.A3_after_the_test_fix` | `src/cratekit/cli/render.py` | user | 5 file(s) | 381 | 1 | killed |
| `r682-a.M10_unstated_never_said` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 3 | killed |
| `r682-a.M11_unstated_bound_inclusive` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 3 | killed |
| `r682-a.M12_bool_is_a_count` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 3 | killed |
| `r682-a.M13_zero_reason_printed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 1 | killed |
| `r682-a.M14_no_breakdown_mapping_gate` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 1 | killed |
| `r682-a.M15_no_state_mapping_gate` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 1 | killed |
| `r682-a.M7_reason_line_not_printed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 6 | killed |
| `r682-a.M8_sorted_by_slug_only` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 1 | killed |
| `r682-a.M9_no_tie_break` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 1 | killed |
| `r686.R1_empty_list_bare_header` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1194 | 3 | killed |
| `r850-a.E11_queued_gate` | `src/cratekit/cli/render.py` | user | 2 file(s) | 180 | 1 | killed |
| `r850-a.E12_count_gate` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r850-a.E13_row_fallback` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r850-a.E14_line_break_quote` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r850-a.E15_rows_not_printed` | `src/cratekit/cli/render.py` | user | 3 file(s) | 291 | 7 | killed |
| `r856-a.R1_hearted_words` | `src/cratekit/cli/render.py` | user | 2 file(s) | 180 | 3 | killed |
| `r856-a.R2_already_hearted_words` | `src/cratekit/cli/render.py` | user | 2 file(s) | 180 | 3 | killed |
| `r925.R2_string_rows` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r925.R3_no_isrc_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 2 | killed |
| `r925.R4_version_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 1 | killed |
| `r925.R5_nameless_row_unsaid` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `r925.R6_count_line` | `src/cratekit/cli/render.py` | user | 2 file(s) | 163 | 2 | killed |
| `u169.R1_job_list_ungated` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R2_job_list_not_rendered` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R3_unreadable_reads_as_none` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R4_skipped_count_dropped` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R5_no_worker_dropped` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u169.R6_filter_unnamed` | `src/cratekit/cli/render.py` | user | 1 file(s) | 55 | 1 | killed |
| `u27-round-8-independent.E7_readonly_sentence_is_permission` | `src/cratekit/cli/render.py` | user | 2 file(s) | 22933 | 0 (promoted) | zero |
| `u49-author.V1_the_terminal_screen_stops_showing_it` | `src/cratekit/cli/render.py` | user | 4 file(s) | 1970 | 3 | killed |
| `u97-a.A1_bare_verb_returns` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 3 | killed |
| `u97-a.A2_rejected_session_says_log_in_again` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 1 | killed |
| `u97-a.A3_procedure_drops_the_erase` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 3 | killed |
| `u97-a.A4_procedure_drops_the_flag` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 4 | killed |
| `u97-a.A5_procedure_drops_the_document` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 4 | killed |
| `u97-a.A6_remedy_text_drops_the_advice` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 9 | killed |
| `u97-b.B2_check_table_prints_no_fix` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 2 | killed |
| `u97-c.C2_remediation_line_drops_the_token_branch` | `src/cratekit/cli/render.py` | user | 3 file(s) | 1588 | 4 | killed |
| `u132.V5_nothing` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 2 | killed |
| `u132.V6_backup_name` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 1 | killed |
| `u133-a.P12_verb_warning` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 1 | killed |
| `u194.W24_write_copy_bytes_stale` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 128 | 1 | killed |
| `u194.W25_write_copy_read_back` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 128 | 2 | killed |
| `r1184.M17_verb_takes_step` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 3 | killed |
| `r1184.M18_verb_nothing_to_do` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W18_carrying_several_genres` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W19_carrying_unread` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 2 | killed |
| `u194.W22_unwritten_refusal` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |
| `u194.W23_root_missing` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 71 | 1 | killed |

## Zero rows and what they owe

- `u27-round-8-independent.E7_readonly_sentence_is_permission` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1334.E1_offer_after_compare`

require (existing, sampled): record the offer only on the open gate, so the decide after a stale binds the shown digest again and every resume is stale

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `E1_offer_after_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
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
- Collected: 1132 against a baseline of 1132
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
- Collected: 1132 against a baseline of 1132
- Kills: 40 (killed)
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
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - ... and 25 more, see the JSON sidecar

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

### `r1334.S10_unknown_option_no_context`

require: raise the unknown option with no screen, as before, though its offer is recorded

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S10_unknown_option_no_context`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`

Old text:

```
            raise UnknownOption(spec, chosen, context)
```

New text:

```
            raise UnknownOption(spec, chosen)
```

### `r1334.S11_unknown_option_shown_dropped`

UnknownOption: ignore the context it is handed

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S11_unknown_option_shown_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`

Old text:

```
        detail: dict[str, Any] = {"gate": spec.name, "options": list(spec.options)}
        if context is not None:
            detail["shown"] = dict(context)
```

New text:

```
        detail: dict[str, Any] = {"gate": spec.name, "options": list(spec.options)}
```

### `r1334.S1_stale_not_offered`

require: raise the digest stale as a verb's own, offered false, so the refusal carries no screen and the decide after it binds an unshown plan (R-1334 itself)

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S1_stale_not_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
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
- Collected: 1132 against a baseline of 1132
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
- Collected: 1132 against a baseline of 1132
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

### `r1334.S4_screen_always`

DecisionStale: add the screen to every stale, a verb's own write handle stale and the pinned one included

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S4_screen_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_pinned_stale_keeps_the_detail_it_had`
  - `tests/test_gate_stale_screen.py::test_a_stale_a_verb_raises_itself_keeps_the_detail_it_had`
  - `tests/test_gate_stale_screen.py::test_only_the_gates_own_stale_prints_a_gate_screen`

Old text:

```
        if offered:
            detail.update(_screen(spec, context))
```

New text:

```
        if True:
            detail.update(_screen(spec, context))
```

### `r1334.S5_screen_no_shown`

_screen: drop the shown plan, keep the options

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S5_screen_no_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
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

### `r1334.S6_screen_shown_empty_for_none`

_screen: an empty shown where the gate shows nothing, absent read as empty

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S6_screen_shown_empty_for_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`

Old text:

```
    if context is not None:
        screen["shown"] = dict(context)
    return screen
```

New text:

```
    screen["shown"] = dict(context or {})
    return screen
```

### `r1334.S7_screen_no_options`

_screen: no options, so the human screen is never printed for a stale

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S7_screen_no_options`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
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

### `r1334.S8_screen_no_prompt`

_screen: no prompt, so the stale screen asks 'A decision is required.'

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S8_screen_no_prompt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`

Old text:

```
        "prompt": spec.prompt,
        "explicit": spec.explicit,
```

New text:

```
        "explicit": spec.explicit,
```

### `r1334.S9_screen_explicit_false`

_screen: every stale read as a gate that takes an inline answer

- File: `src/cratekit/cli/gates.py`
- Source: `r1334.json`, row `S9_screen_explicit_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_organize.py`, `tests/test_gate_pins.py`, `tests/test_gate_shown_plan.py`, `tests/test_cli_contract.py`
- Collected: 1132 against a baseline of 1132
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`

Old text:

```
        "explicit": spec.explicit,
    }
```

New text:

```
        "explicit": False,
    }
```

### `r1349.C1_argv_ignored`

continue_command: the recorded command line ignored, so every continue says the verb's words and an ellipsis

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `C1_argv_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
- Kills: 49 (killed)
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
  - ... and 34 more, see the JSON sidecar

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
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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

### `r1349.N3_offer_ignored`

record: the offer clause dropped, so a run handed an offer (hand_off) or a gate offered and not open is refused

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N3_offer_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_handed_off_run_holds_the_offer_its_decide_binds`

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
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `r1349.N4_open_ignored`

record: the open gate clause dropped, so a gate reached with no digest and left open is refused

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N4_open_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
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

### `r1349.N5_answered_ignored`

record: the answered clause dropped, so a gate reached with no digest and answered cannot be answered again

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N5_answered_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_already_answered_takes_a_new_answer_once_the_run_waits_elsewhere`

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
        and state.open_gate != spec.name
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
- Collected: 1213 against a baseline of 1213
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

### `r1349.N7_written_before_refusal`

record: the answer written before the refusal is raised, so the refusal leaves a digestless decision in the run

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N7_written_before_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one`
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`

Old text:

```
        raise GateNotReached(state, spec)

```

New text:

```
        state.decisions[spec.name] = Decision(option=option, actor=actor, recorded="", digest=None)
        raise GateNotReached(state, spec)

```

### `r1349.N8_after_unknown_swapped`

record: the unknown option check skipped, so an option the gate does not offer is recorded

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N8_after_unknown_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_an_unknown_option_is_refused_as_it_was_on_a_gate_not_reached`

Old text:

```
    if option not in spec.options:
        raise UnknownOption(spec, option)
    if (

```

New text:

```
    if False:
        raise UnknownOption(spec, option)
    if (

```

### `r1349.R1_reason_open_gate`

GateNotReached: reason decision-required, read and printed as an open gate inviting the refused answer

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R1_reason_open_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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
- Collected: 1213 against a baseline of 1213
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

### `r1349.R6_message_no_gate`

GateNotReached: the message names no gate

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R6_message_no_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing`
  - `tests/test_gate_not_reached.py::test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`

Old text:

```
                    f"run {state.run_id} has not reached the gate {spec.name!r}, so "
```

New text:

```
                    f"run {state.run_id} has not reached a gate yet, so "
```

### `r1349.R7_answer_step_dropped`

GateNotReached: the closing step that answers the named gate dropped when the run waits at another

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `R7_answer_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1213 against a baseline of 1213
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one`

Old text:

```
                f"then {reach}",
                answer,

```

New text:

```
                f"then {reach}",

```

### `u112.G1_part_unverified`

hand_off carries any digest a caller names as the part, whatever the answer was given over

- File: `src/cratekit/cli/gates.py`
- Source: `u112.json`, row `G1_part_unverified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_sync_all.py`
- Collected: 215 against a baseline of 215
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

### `u161.G1_pin_never_compared`

Gates.require: skip the pin comparison, so an answer given over one file is used by a run that opened another

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G1_pin_never_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`, `tests/test_gate_shown_plan.py`
- Collected: 81 against a baseline of 81
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`

Old text:

```
        if recorded is not None and inline is None:
            held = self.state.pins.get(spec.name, {})
```

New text:

```
        if False:
            held = self.state.pins.get(spec.name, {})
```

### `u161.G2_pin_overwritten_before_compare`

Gates.require: record the pin on every call, so the continuation replaces the answered pin before comparing it

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G2_pin_overwritten_before_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`, `tests/test_gate_shown_plan.py`
- Collected: 81 against a baseline of 81
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`

Old text:

```
        if recorded is None and pins:
```

New text:

```
        if pins:
```

### `u161.G3_absence_read_as_agreement`

Gates.require: compare only keys both sides pinned, so a run that pinned nothing passes a gate that now pins

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G3_absence_read_as_agreement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`, `tests/test_gate_shown_plan.py`
- Collected: 81 against a baseline of 81
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`

Old text:

```
                if held.get(key) != pins.get(key):
```

New text:

```
                if key in held and key in pins and held[key] != pins[key]:
```

### `u161.G4_pins_not_written`

RunState.to_json: never write the pins, so the answer's file is lost when the first act exits

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G4_pins_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`, `tests/test_gate_shown_plan.py`
- Collected: 81 against a baseline of 81
- Kills: 28 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_pins.py::test_the_same_pin_on_the_continuation_takes_the_recorded_answer`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_intake_land_native.py::test_a_landing_given_no_pass_names_none`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        if self.pins:
            record["pins"]
```

New text:

```
        if False:
            record["pins"]
```

### `u161.G5_pins_not_read`

RunState.from_json: read no pins back, so a continuation sees none

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G5_pins_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`, `tests/test_gate_shown_plan.py`
- Collected: 81 against a baseline of 81
- Kills: 28 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_pins.py::test_the_same_pin_on_the_continuation_takes_the_recorded_answer`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_intake_land_native.py::test_a_landing_given_no_pass_names_none`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column`
  - ... and 13 more, see the JSON sidecar

Old text:

```
                for name, one in (data.get("pins") or {}).items()
```

New text:

```
                for name, one in {}.items()
```

### `u168.C12_argv_not_saved`

RunState.to_json: drop the command line from the saved record

- File: `src/cratekit/cli/gates.py`
- Source: `u168.json`, row `C12_argv_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`, `tests/test_gate_pins.py`
- Collected: 1012 against a baseline of 1012
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

### `u170.G1_threshold_boundary`

old_gate: a gate idle exactly the threshold counts as old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G1_threshold_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_exactly_at_the_threshold_is_not_yet_old`

Old text:

```
    if now - since <= older_than:
```

New text:

```
    if now - since < older_than:
```

### `u170.G2_idle_from_start_only`

idle_since: age from created alone, so a resumed run is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G2_idle_from_start_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
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
- Collected: 1704 against a baseline of 1704
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
- Collected: 1704 against a baseline of 1704
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
- Collected: 1704 against a baseline of 1704
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
- Collected: 1704 against a baseline of 1704
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
- Collected: 1704 against a baseline of 1704
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

### `u186.S10_scope_every_verb`

writes_the_database: answer True for every declared verb, so a gated verb writing no database warns

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S10_scope_every_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_verb_that_writes_no_database_is_outside_the_warning`
  - `tests/test_gate_siblings.py::test_a_verb_writing_no_database_says_nothing_of_its_own_siblings`

Old text:

```
    return bool(owner.writes & DB_WRITE_SURFACES)
```

New text:

```
    return True
```

### `u186.S1_window_wider`

SIBLING_WINDOW: twelve hours widened to a day, so an answer thirteen hours old is named

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S1_window_wider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_over_a_sibling_answered_thirteen_hours_ago`

Old text:

```
SIBLING_WINDOW = timedelta(hours=12)
```

New text:

```
SIBLING_WINDOW = timedelta(hours=24)
```

### `u186.S2_window_narrower`

SIBLING_WINDOW: twelve hours halved, so an answer eleven hours fifty old is silent

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S2_window_narrower`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_an_answer_just_inside_twelve_hours_is_still_named`

Old text:

```
SIBLING_WINDOW = timedelta(hours=12)
```

New text:

```
SIBLING_WINDOW = timedelta(hours=6)
```

### `u186.S3_exclude_self`

siblings: drop the asking run's exclusion, so a run continued to its gate names itself

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S3_exclude_self`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 19 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`
  - `tests/test_gate_siblings.py::test_a_run_never_warns_about_itself`
  - `tests/test_gate_siblings.py::test_a_run_of_another_verb_is_never_named`
  - `tests/test_gate_siblings.py::test_a_sibling_whose_gate_is_open_is_named_as_open`
  - `tests/test_gate_siblings.py::test_an_answer_just_inside_twelve_hours_is_still_named`
  - `tests/test_gate_siblings.py::test_an_answer_ten_minutes_ago_is_named_with_its_actor_option_and_time`
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_an_answer_with_no_recorded_time_is_named_as_unrecorded`
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_continue_says_a_sibling_once_when_the_verb_stops_at_its_gate_again`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_over_a_sibling_answered_thirteen_hours_ago`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_aborted`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        if path.stem == exclude:
            continue
        try:
            state = load(path.stem)
```

New text:

```
        try:
            state = load(path.stem)
```

### `u186.S4_other_verb`

siblings: drop the verb filter, so a run of another verb is named

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S4_other_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_run_of_another_verb_is_never_named`

Old text:

```
        if state.verb != verb:
            continue
```

New text:

```
(empty)
```

### `u186.S5_unreadable_dropped`

siblings: skip a record that cannot be read rather than counting it, so the gap reads as no sibling

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S5_unreadable_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`

Old text:

```
        except Exception:  # noqa: BLE001 - an unread record is said, never skipped
            unreadable.append(path.stem)
            continue
```

New text:

```
        except Exception:  # noqa: BLE001 - an unread record is said, never skipped
            continue
```

### `u186.S6_unrecorded_time_old`

siblings: an answer whose time cannot be read counts as old rather than recent

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S6_unrecorded_time_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_an_answer_with_no_recorded_time_is_named_as_unrecorded`

Old text:

```
            if when is None or moment - when <= within:
```

New text:

```
            if when is not None and moment - when <= within:
```

### `u186.S7_open_drops_answers`

siblings: a run with an open gate keeps no answers, the shape the first review round drove

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S7_open_drops_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`

Old text:

```
                    run_id=state.run_id, verb=verb, gate=state.open_gate, at=since, answers=answers
```

New text:

```
                    run_id=state.run_id, verb=verb, gate=state.open_gate, at=since, answers=()
```

### `u186.S8_open_read_as_answered`

siblings: an open gate is reported as an answered run, so the message never says open

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S8_open_read_as_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_sibling_whose_gate_is_open_is_named_as_open`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_one_warning_per_other_run`
  - `tests/test_gate_siblings.py::test_the_warning_prints_on_the_screen_a_person_reads`

Old text:

```
        if state.open_gate is not None:
            since = idle_since(state, path)
```

New text:

```
        if False:
            since = idle_since(state, path)
```

### `u186.S9_unreadable_unsaid`

sibling_warnings: say nothing of the records that could not be read

- File: `src/cratekit/cli/gates.py`
- Source: `u186.json`, row `S9_unreadable_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`

Old text:

```
    if unreadable:
        records_word = "record" if len(unreadable) == 1 else "records"
        said.append(
```

New text:

```
    if False:
        records_word = "record" if len(unreadable) == 1 else "records"
        said.append(
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

### `u49-author.G2_the_second_raise_site_drops_the_context`

Carry the context at the no-answer refusal only, so what a person sees depends on whether they typed a flag

- File: `src/cratekit/cli/gates.py`
- Source: `u49-author.json`, row `G2_the_second_raise_site_drops_the_context`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 1987 against a baseline of 1987
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_explicit_inline_refusal_carries_the_context_too`

Old text:

```
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id, context)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
```

New text:

```
            self.state.open_gate = spec.name
            raise DecisionRequired(spec, self.state.run_id)

        chosen = inline if inline is not None else (recorded.option if recorded else None)
```

### `u270.H1_batch_size_floor`

batching_of: accept a batch form of size zero

- File: `src/cratekit/cli/handlers.py`
- Source: `u270.json`, row `H1_batch_size_floor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_batch_form_that_is_not_a_callable_and_a_size_refuses[size-zero]`

Old text:

```
isinstance(size, bool) or size < 1:
```

New text:

```
isinstance(size, bool) or size < 0:
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

### `u274.H1_drive_not_entered`

run_job: never enter the worker's per drive holder

- File: `src/cratekit/cli/handlers.py`
- Source: `u274.json`, row `H1_drive_not_entered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
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
- Collected: 449 against a baseline of 449
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

### `u46-author.H1_binding_removed`

Unbind master, so no verb in the build has a handler at all

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H1_binding_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 107 against a baseline of 107
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
- Collected: 107 against a baseline of 107
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

### `u46-author.H3_import_before_refusing`

Import the declared module before checking the key is real, defeating KTD26

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H3_import_before_refusing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 107 against a baseline of 107
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_resolving_a_handler_key_imports_nothing_a_supervisor_does_not_need`

Old text:

```
def is_known(key: str) -> bool:
```

New text:

```
def is_known(key: str) -> bool:
    importlib.import_module("cratekit.master.cli")
```

### `u46-author.H4_unbound_reason_silent`

Stop saying why a queued verb has no worker

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H4_unbound_reason_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 107 against a baseline of 107
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

### `u46-author.H5_fresh_config`

Hand the handler a freshly loaded configuration instead of the frozen one

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H5_fresh_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 107 against a baseline of 107
- Kills: 2 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_worker_naming_a_batch_form_is_driven_in_batches_against_the_frozen_config`
  - `tests/test_handlers.py::test_the_handler_receives_the_frozen_configuration_and_not_the_current_one`

Old text:

```
    frozen = jobs.frozen_config(job)
```

New text:

```
    frozen = config.load()
```

### `u46-author.H7_no_drift`

Never compute drift, so a moved configuration is silently chosen between

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H7_no_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 107 against a baseline of 107
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

### `u46-author.H8_drift_wording_dropped`

Report drift without naming what moved

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H8_drift_wording_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 107 against a baseline of 107
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between`

Old text:

```
                f"configuration changed since this job was queued; it runs against "
                f"the frozen copy. Changed: {', '.join(keys)}"
```

New text:

```
                f"the frozen configuration was used for this run"
```

### `u52-item-derivation.B1_label_import_unbound`

Unbind label.import, leaving a queued job with a worker in neither table

- File: `src/cratekit/cli/handlers.py`
- Source: `u52-item-derivation.json`, row `B1_label_import_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 314 against a baseline of 314
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
- Collected: 314 against a baseline of 314
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
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_track_read_raises_in_kind_keeps_its_own_reason`
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
- Collected: 314 against a baseline of 314
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
  - `tests/test_label_workers.py::test_a_release_that_is_gone_breaks_the_run_of_failed_reads`
  - `tests/test_label_workers.py::test_a_release_the_library_holds_only_in_another_version_is_offered`
  - `tests/test_label_workers.py::test_a_release_with_a_row_the_reader_cannot_read_is_offered`
  - ... and 27 more, see the JSON sidecar

Old text:

```
    "sync.labels": "cratekit.label.cli:handle",
```

New text:

```
    "sync.labels": "cratekit.favorites.cli:handle",
```

### `u55-collection-reader.R30_scan_handler_bound`

adopt.scan loses its worker, which is the state R-203 records

- File: `src/cratekit/cli/handlers.py`
- Source: `u55-collection-reader.json`, row `R30_scan_handler_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 286 against a baseline of 286
- Kills: 9 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_adopt_workers.py::test_a_scan_parses_the_active_taxonomy_once_however_many_rows_it_drives`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_both_adopt_keys_resolve_to_a_worker`
  - `tests/test_adopt_workers.py::test_the_configuration_reaching_the_scan_worker_is_the_frozen_one`
  - `tests/test_adopt_workers.py::test_the_reported_counts_come_from_the_artifacts_and_not_from_the_queue`
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "adopt.scan": "cratekit.adopt.scan_cli:handle",
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
- Collected: 388 against a baseline of 388
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
- Collected: 388 against a baseline of 388
- Kills: 21 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_made_blank_between_the_confirm_and_the_drive_is_left_to_its_owner`
  - `tests/test_tag_workers.py::test_a_genre_made_specific_between_the_confirm_and_the_drive_is_not_rewritten`
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

### `u58-workers-and-wav.H1_run_unbound`

Drop the analyze.run binding from the handler table

- File: `src/cratekit/cli/handlers.py`
- Source: `u58-workers-and-wav.json`, row `H1_run_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 642 against a baseline of 642
- Kills: 33 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_calibrated_level_is_written_and_routes_to_a_band`
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    "analyze.run": "cratekit.analysis.cli:handle_run",

```

New text:

```
(empty)
```

### `r290-author.S07_rebuild_call_removed`

Remove the one jobs.raise_for_state call from cli/rebuild.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/cli/rebuild.py`
- Source: `r290-author.json`, row `S07_rebuild_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[rebuild]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[rebuild]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `u132.W5_rebuild_note`

The rebuild resume carries no skipped step note

- File: `src/cratekit/cli/rebuild.py`
- Source: `u132.json`, row `W5_rebuild_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`

Old text:

```
            *engine.favorites_skipped_warnings(declared, driven),

```

New text:

```
(empty)
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

### `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped`

The rebuild files a job with no items, the state every rebuild was in before this unit

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `I3_rebuild_items_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 21 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_over_an_absent_music_directory_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_watches_the_grids_where_they_actually_live`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`
  - `tests/test_routing_workers.py::test_a_resume_reads_no_registry_of_its_own`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            payload={"tree": tree_id, "actor": actor},
            item_ids=items,
```

New text:

```
            payload={"tree": tree_id, "actor": actor},
```

### `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job`

The rebuild drives another verb's job, without that verb's own resume checks

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R2_rebuild_drives_a_foreign_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_another_verbs_job[rebuild]`

Old text:

```
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
```

New text:

```
    if False:
        raise refuse(
            "job-unknown",
```

### `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job`

A rebuild queued by an older build drives to succeeded having rebuilt nothing

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R4_rebuild_drives_an_itemless_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_a_job_an_older_build_queued_with_no_items[rebuild]`

Old text:

```
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
```

New text:

```
        if False:
            raise refuse(
                "internal-error",
```

### `u53-zero-rows-remeasured.I6_tree_items_ignores_native`

The rebuild's items include trees the registry says are still on the bridge

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-zero-rows-remeasured.json`, row `I6_tree_items_ignores_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge[rebuild]`

Old text:

```
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    native = tuple(sorted(entries.tree_ids()))
```

### `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree`

A rebuild of one named tree quietly rebuilds every tree in the library

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-zero-rows-remeasured.json`, row `I7_tree_items_ignores_the_named_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`

Old text:

```
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)
```

New text:

```
    return native
```

### `u89.W4_rebuild_worker`

cli/rebuild handle: hand the engine None instead of the loaded cut

- File: `src/cratekit/cli/rebuild.py`
- Source: `u89.json`, row `W4_rebuild_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_worker_driven_without_the_resume_refuses_a_corrupt_calibration`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
        vocal_threshold=None,
```

### `u89.W6_rebuild_resume_loads_first`

cli/rebuild _resume: do not read the cut before driving, so a corrupt calibration fails items instead of refusing

- File: `src/cratekit/cli/rebuild.py`
- Source: `u89.json`, row `W6_rebuild_resume_loads_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_resume_that_drove_nothing_carries_no_vocal_warning[rebuild]`

Old text:

```
        threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
```

New text:

```
        threshold = 0.0
```

### `r1334.S12_render_no_stale_header`

render_gate: no line saying the plan moved and that an answer now is taken over it

- File: `src/cratekit/cli/render.py`
- Source: `r1334.json`, row `S12_render_no_stale_header`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`, `tests/test_gate_shown_plan.py`
- Collected: 1025 against a baseline of 1025
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
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`, `tests/test_gate_shown_plan.py`
- Collected: 1025 against a baseline of 1025
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
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`, `tests/test_gate_shown_plan.py`
- Collected: 1025 against a baseline of 1025
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
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`, `tests/test_gate_shown_plan.py`
- Collected: 1025 against a baseline of 1025
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
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`, `tests/test_gate_shown_plan.py`
- Collected: 1025 against a baseline of 1025
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
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`, `tests/test_gate_shown_plan.py`
- Collected: 1025 against a baseline of 1025
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
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`
- Collected: 1010 against a baseline of 1010
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
  - `tests/test_label_workers.py::test_an_empty_harvest_still_names_that_nothing_was_offered`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label`
  - `tests/test_label_workers.py::test_harvest_human_output_names_the_unresolved_count_and_not_an_unconfirmed_imprint`

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
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label`
  - `tests/test_label_workers.py::test_harvest_human_output_names_the_unresolved_count_and_not_an_unconfirmed_imprint`

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
  - `tests/test_label_workers.py::test_an_empty_harvest_still_names_that_nothing_was_offered`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label`
  - `tests/test_label_workers.py::test_harvest_human_output_names_the_unresolved_count_and_not_an_unconfirmed_imprint`

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
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label`
  - `tests/test_label_workers.py::test_harvest_human_output_names_the_unresolved_count_and_not_an_unconfirmed_imprint`

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
  - `tests/test_label_workers.py::test_an_empty_harvest_still_names_that_nothing_was_offered`
  - `tests/test_label_workers.py::test_harvest_human_output_names_each_offered_label`

Old text:

```
    if queue not in (None, ""):
        lines.append(f"  queue: {_shown_value(queue)}")

```

New text:

```
(empty)
```

### `r395.M11_render_literal`

Put the old bare pip literal back in the parser stub

- File: `src/cratekit/cli/render.py`
- Source: `r395.json`, row `M11_render_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_install_command.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_reserved_causes.py`
- Collected: 2239 against a baseline of 2239
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

### `r678-a.A10_proof_ungated_on_verb`

every plan verb's items are rendered as import proof lines

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A10_proof_ungated_on_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 102 against a baseline of 102
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
- Collected: 102 against a baseline of 102
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
- Collected: 102 against a baseline of 102
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
- Collected: 381 against a baseline of 381
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_favorites_names_the_job_and_the_command_that_drives_it`
  - `tests/intake/test_workers.py::test_the_resolution_names_owned_offered_and_missing_and_the_next_command`
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

### `r678-a.A2_drop_the_import_proof_case`

the original defect for intake imported: render never asks for the proof

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A2_drop_the_import_proof_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 102 against a baseline of 102
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

### `r678-a.A4_empty_job_id_renders_a_job`

a queue that held nothing prints a job line with an empty identifier

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A4_empty_job_id_renders_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 381 against a baseline of 381
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_empty_playlist_names_no_job_because_none_was_queued`
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
- Collected: 381 against a baseline of 381
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
- Collected: 381 against a baseline of 381
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
- Collected: 381 against a baseline of 381
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
- Collected: 163 against a baseline of 163
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
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
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
- Collected: 163 against a baseline of 163
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
- Collected: 163 against a baseline of 163
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
- Collected: 163 against a baseline of 163
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
- Collected: 163 against a baseline of 163
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
- Collected: 163 against a baseline of 163
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
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
- Collected: 163 against a baseline of 163
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
- Collected: 163 against a baseline of 163
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

### `r686.R1_empty_list_bare_header`

An empty collection in a gate's context renders as a bare header again

- File: `src/cratekit/cli/render.py`
- Source: `r686.json`, row `R1_empty_list_bare_header`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`
- Collected: 1194 against a baseline of 1194
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_screen_says_none_for_an_empty_warning_list`

Old text:

```
        if isinstance(value, (Mapping, list, tuple)) and not value:

```

New text:

```
        if False:

```

### `r850-a.E11_queued_gate`

render.render_job_state: print the counts for a queued job too, so its zeros read as a finished export

- File: `src/cratekit/cli/render.py`
- Source: `r850-a.json`, row `E11_queued_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_outbound_workers.py`
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 180 against a baseline of 180
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
- Collected: 163 against a baseline of 163
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

### `r925.R4_version_unsaid`

The human line drops a track's version

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R4_version_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`

Old text:

```
        if row.get("version"):
            named += f" ({_one_line(row['version'])})"
```

New text:

```
        if False:
            named += f" ({_one_line(row['version'])})"
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
- Collected: 163 against a baseline of 163
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

### `u27-round-8-independent.E7_readonly_sentence_is_permission`

Give a read only volume the permission-grant sentence, the defect round 8 closed one layer up

- File: `src/cratekit/cli/render.py`
- Source: `u27-round-8-independent.json`, row `E7_readonly_sentence_is_permission`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 22933 against a baseline of 22933
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
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`
- Collected: 1970 against a baseline of 1970
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
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
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

### `u97-a.A2_rejected_session_says_log_in_again`

_ADVICE: put REAUTHENTICATE_PROVIDER back to log in again, the same instruction nothing performs on the likelier path

- File: `src/cratekit/cli/render.py`
- Source: `u97-a.json`, row `A2_rejected_session_says_log_in_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
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
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
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
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
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
- Collected: 1588 against a baseline of 1588
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
- Collected: 1588 against a baseline of 1588
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

### `u97-b.B2_check_table_prints_no_fix`

render_checks: print the check row and swallow its fix line, so the human report names every failure and no remedy

- File: `src/cratekit/cli/render.py`
- Source: `u97-b.json`, row `B2_check_table_prints_no_fix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
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
- Ran: `tests/test_cli_contract.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 1588 against a baseline of 1588
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

### `u132.V5_nothing`

A plan that writes nothing still asks the gate

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V5_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_what_is_held_is_said_and_written_around`

Old text:

```
    if not found.writes:

```

New text:

```
    if False:

```

### `u132.V6_backup_name`

A backup takes the name an earlier backup holds

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V6_backup_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_backup_never_takes_an_earlier_backups_name`

Old text:

```
    while candidate.exists():

```

New text:

```
    while False:

```

### `u133-a.P12_verb_warning`

The verb drops the keyword rule warning

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u133-a.json`, row `P12_verb_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
    ] + [{"code": KEYWORD_RULE, "message": sentence} for sentence in found.keywords]

```

New text:

```
    ]

```

### `u194.W24_write_copy_bytes_stale`

write_copy: drop the byte check after the second plan, so an edit made since is written over

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W24_write_copy_bytes_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`

Old text:

```
    if as_read(raw) != before:
```

New text:

```
    if False:
```

### `u194.W25_write_copy_read_back`

write_copy: drop the read back, so a copy that does not load is left as every verb's declaration

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W25_write_copy_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 128 against a baseline of 128
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`

Old text:

```
    problem = _read_back(cfg, path, written)
    if problem is not None:
```

New text:

```
    problem = _read_back(cfg, path, written)
    if False:
```

### `r1184.M17_verb_takes_step`

taxonomy alias verb: ignore the refusal's own step, so the bare folder and own name refusals say leave the word

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M17_verb_takes_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_the_bare_folder_refusal_names_the_folder_verb_as_its_step`

Old text:

```
    if exc.step:

```

New text:

```
    if False:

```

### `r1184.M18_verb_nothing_to_do`

taxonomy alias verb: the no change sentence for an own name claims a tagging alias

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M18_verb_nothing_to_do`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`

Old text:

```
                        if edit.own_name

```

New text:

```
                        if False

```

### `u194.W18_carrying_several_genres`

carrying: plan a write for a file carrying the word beside another genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W18_carrying_several_genres`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_with_two_genres_is_left_and_named`

Old text:

```
        current = _JOINED.join(values)
        if len(values) == 1:
```

New text:

```
        current = _JOINED.join(values)
        if True:
```

### `u194.W19_carrying_unread`

carrying: read a file whose genre could not be read as one carrying no genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W19_carrying_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_whose_genre_cannot_be_read_is_named_and_never_called_clean`
  - `tests/test_taxonomy_word.py::test_nothing_to_do_does_not_claim_a_file_it_could_not_read`

Old text:

```
        if values is None:
            items.append(FileItem(path=path, relative=relative, change=UNREAD))
            continue
```

New text:

```
        if values is None:
            continue
```

### `u194.W22_unwritten_refusal`

alias verb: leave a file the writer could not write out of the refusal, so the run reports success

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W22_unwritten_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes`

Old text:

```
    if done.moved or done.failed or done.wrong:
```

New text:

```
    if done.moved or done.wrong:
```

### `u194.W23_root_missing`

_root: drop the refusal of a folder that is not there, so the walk plans nothing and reads clean

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W23_root_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folder_that_is_not_there_is_refused_with_nothing_written`

Old text:

```
    if not root.is_dir():
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

New text:

```
    if False:
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

