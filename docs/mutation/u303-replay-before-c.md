# Mutation table: u303-replay-before-c

Measured by `scripts/mutate.py` on 2026-11-22 22:09 UTC, branch `cloud/860-replay-c` at `fd8173d3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 205.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 37, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `../known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1334.S18_emit_open_gate_only` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1010 | 1 | killed |
| `r1694.C1_no_warning` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 134 | 3 | killed |
| `r1694.C2_every_note` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 134 | 2 | killed |
| `r1694.C3_no_dedupe` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 134 | 1 | killed |
| `r1694.C4_words_no_next_run` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 134 | 1 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7393 | 47 | killed |
| `r290-author.D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7393 | 2 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7393 | 22 | killed |
| `r678-b.B1_emit_hands_in_no_drive` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 334 | 3 | killed |
| `r678-b.B2_drive_for_a_verb_that_did_not_queue` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 334 | 1 | killed |
| `r678-b.B3_narrow_catch` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 334 | 1 | killed |
| `r705-b.S11_spend_line_always_suppressed` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 117 | 5 | killed |
| `r705-b.S12_dispatcher_never_adds_the_spend` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 117 | 5 | killed |
| `r924.D1_json_gets_progress` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 57 | 1 | killed |
| `r924.D2_human_gets_none` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 57 | 5 | killed |
| `r924.D3_write_failure_raises` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 11 | 1 | killed |
| `u168.C10_argv_never` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1005 | 5 | killed |
| `u168.C11_argv_whole_line` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1005 | 3 | killed |
| `u168.C9_argv_on_every_run` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1005 | 1 | killed |
| `u186.D1_dispatch_unhooked` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 9 | killed |
| `u186.D2_dispatch_any_refusal` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.D3_dispatch_scope` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.D4_dispatch_break_silent` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 34 | 1 | killed |
| `u193.M16_continue_job_branch` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M19_parked_outcome` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M20_continue_step_not_written` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 508 | 3 | killed |
| `u193.M21_swallowed_warning_dropped` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M22_warning_said_twice` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 508 | 1 | killed |
| `u193.M23_calls_floor` | `src/cratekit/cli/__init__.py` | user | 5 file(s) | 508 | 1 | killed |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u210.R24_continue_run` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 131 | 1 | killed |
| `u211.D1_refusal_keeps_its_run` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1180 | 2 | killed |
| `u211.D2_continue_step_named` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1180 | 2 | killed |
| `u211.D4_only_the_scans_own_refusal_is_kept` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 150 | 1 | killed |
| `u248.L10_built_before_the_builder` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 158 | 1 | killed |
| `u248.L1_lazy_off` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1155 | 12 | killed |
| `u248.L2_chosen_never_built` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1155 | 306 | killed |
| `u248.L3_listing_asks_everyone` | `src/cratekit/cli/__init__.py` | maintainer | 2 file(s) | 1155 | 4 | killed |
| `u248.L4_listing_drops_the_stub_line` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1206 | 4 | killed |
| `u248.L5_listing_asked_twice` | `src/cratekit/cli/__init__.py` | maintainer | 1 file(s) | 158 | 2 | killed |
| `u248.L6_built_twice` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1155 | 1 | killed |
| `u248.L7_defect_as_stub` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1155 | 2 | killed |
| `u248.L8_listing_raises_a_defect` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1155 | 1 | killed |
| `u248.L9_argument_error_unwrapped` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1155 | 2 | killed |
| `u274.I1_context_drops_warnings` | `src/cratekit/cli/__init__.py` | user | 6 file(s) | 449 | 3 | killed |
| `u278.M20_report_spends_reserve` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 1174 | 1 | killed |
| `u278.M21_downloads_not_reserve` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 1174 | 2 | killed |
| `u278.M22_no_upfront_refusal` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 177 | 2 | killed |
| `r118-b.C1_wizard_probe_escapes` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r118-b.C3_wizard_probe_note_is_advisory` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r345.B1_flags_recorded` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1465 | 6 | killed |
| `r345.B2_module_off` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1465 | 3 | killed |
| `r345.B3_recorded_kept` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1465 | 2 | killed |
| `r345.B4_offer_not_demand` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1465 | 10 | killed |
| `r345.B5_remote_into_document` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1465 | 3 | killed |
| `r345.B6_unknown_module_filter` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 1465 | 1 | killed |
| `r372-b.B10_setup_records_a_literal_root` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 3 | killed |
| `r372-b.B11_setup_records_without_asking` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B6_setup_overwrites_a_recorded_map` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B8_setup_aborts_on_a_copy_it_could_not_make` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 1 | killed |
| `r372-b.B9_setup_offers_a_rule_the_root_does_not_need` | `src/cratekit/cli/setup.py` | user | 3 file(s) | 494 | 2 | killed |
| `r662-a.M6_flag_not_recorded` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-a.M8_known_spelled_remote_replaced` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-a.M9_replaced_toward_unknown_remote` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 1 | killed |
| `r662-b.M10_composite_with_M9` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M11_replacement_silent` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M12_replacement_not_written` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M13_fix_line_back_to_setup` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M14_token_dropped_beside_others` | `src/cratekit/cli/setup.py` | maintainer | 1 file(s) | 417 | 1 | killed |
| `r662-b.M15_advice_names_spelled_remote` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M16_flag_not_declared` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 1414 | 14 | killed |
| `r662-b.M18_repair_never_runs` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r662-b.M7_composite_with_M9` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 3 | killed |
| `r663-a.M11_setup_never_checks` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 51 | 2 | killed |
| `r663-a.M12_setup_stops_on_every_refusal` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 51 | 1 | killed |
| `r83.P3_empty_secret_note_status` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `r83.P4_empty_secret_branch` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 417 | 2 | killed |
| `u154.G16_wizard_default_dropped` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 6 | 1 | killed |
| `u27-round-8-independent.S1_act_always_generic` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u27-round-8-independent.S2_template_write_no_error` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u27-round-8-independent.S3_unreachable_root_hardcoded` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u283.S10_any_raise_escapes` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 2 | killed |
| `u283.S11_vocabulary_never_noted` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 2 | killed |
| `u283.S12_vocabulary_always_noted` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S13_linked_copy_not_checked` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S14_no_explanation` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S15_nothing_entered_fails` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 2 | killed |
| `u283.S16_refusal_line_leaks` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 3 | killed |
| `u283.S17_verb_skips_step` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 4 | killed |
| `u283.S1_loop_offers_discogs_again` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 3 | killed |
| `u283.S2_step_ignores_offered` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S3_relink_flag_ignored` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 7 | killed |
| `u283.S4_recorded_never_acknowledged` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 3 | killed |
| `u283.S5_rejected_falls_through_to_store` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 4 | killed |
| `u283.S6_relink_stores_unchecked` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 3 | killed |
| `u283.S7_accepted_note_swapped` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 8 | killed |
| `u283.S8_more_tries` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S9_default_no` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `r1115.S1_sync_land_stops_on_unsettled` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1115.S2_sync_land_names_the_refused` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1499.S01_download_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 12 | killed |
| `r1499.S02_tail_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S03_arrival_after_tail` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S04_arrival_after_plan` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S05_keep_after_arrival` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S06_keep_called` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 7 | killed |
| `r1499.S07_kept_read` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 4 | killed |
| `r1499.S08_own_pass_proof` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S09_own_library` | `src/cratekit/cli/sync_land.py` | maintainer | 6 file(s) | 324 | 1 | killed |
| `r1499.S10_own_by_list` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 66 | killed |
| `r1499.S11_unreadable_refuses` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S12_warnings_in_refusal` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S13_own_unnamed_step` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `u152.R13_missing_lift` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R14_download_list_match` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R15_download_newest` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R16_download_cancelled` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R17_download_retry` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R20_nothing_downloaded` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 2 | killed |
| `u152.R2_preflight_backup` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R6_lift_failed_checks` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 2 | killed |
| `u152.R7_outbound_held` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 2 | killed |
| `u152.R8_continue_open_pass` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u152.R9_open_passes_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1183 | 1 | killed |
| `u179.P1_shared_preflight` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 104 | 3 | killed |
| `u181.S1_profile_off_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1068 | 1 | killed |
| `u181.S2_gate_never_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1068 | 6 | killed |
| `u181.S3_stop_goes_on` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M18_left_open_taken` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M19_left_open_identity` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M20_cancelled_driven` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M21_all_cancelled_done` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M22_skip_failed` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M11_land_runs_named` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u183.M12_preflight_way_back` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M14_retryable_intake_continues` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M15_continue_command_words` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 9 | killed |
| `u183.M1_pass_run_as_given` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 16 | killed |
| `u183.M2_land_record_resolves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 3 | killed |
| `u183.M3_recorded_pass_needs_a_job` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M6_unreadable_record` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M7_remember_saves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M8_remember_called` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 5 | killed |
| `u212.S1_missing_ends` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 334 | 1 | killed |
| `u212.S2_download_refused_all` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 22933 | 0 (promoted) | zero |
| `u212.S3_no_list_download` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 22933 | 0 (promoted) | zero |
| `u212.S4_staged_said` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 334 | 1 | killed |
| `u227.R15_way_on_wording` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R19_take_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R20_take_source` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 2 | killed |
| `u227.R21_take_continued` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R22_take_not_driven` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R25_way_on_state` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u293.S3_sync_land_holds` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 144 | 1 | killed |
| `u293.N1_no_answer` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 4 | killed |
| `u293.N2_rekordbox_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 3 | killed |
| `u293.N3_live_job_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 1 | killed |
| `u293.N4_occupied_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 4 | killed |
| `u293.N5_owed_kept` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 3 | killed |
| `u293.N6_settled_by_landing` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 1 | killed |
| `u293.N7_unread_landing_is_not_settled` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1068 | 1 | killed |

## Zero rows and what they owe

- `u27-round-8-independent.S1_act_always_generic` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.S2_template_write_no_error` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u27-round-8-independent.S3_unreachable_root_hardcoded` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u212.S2_download_refused_all` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u212.S3_no_list_download` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1334.S18_emit_open_gate_only`

_emit: print the gate screen for an open gate only, as before

- File: `src/cratekit/cli/__init__.py`
- Source: `r1334.json`, row `S18_emit_open_gate_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_stale_screen.py`, `tests/test_cli_contract.py`
- Collected: 1010 against a baseline of 1010
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_stale_screen.py::test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it`

Old text:

```
    if envelope.cause is not None and render.is_gate_screen(envelope.cause):
```

New text:

```
    if envelope.cause is not None and envelope.cause.reason == "decision-required":
```

### `r1694.C1_no_warning`

dispatcher: never add the warning, so a verb whose login failed to store says nothing

- File: `src/cratekit/cli/__init__.py`
- Source: `r1694.json`, row `C1_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_gate.py`
- Collected: 134 against a baseline of 134
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
- Collected: 134 against a baseline of 134
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
- Collected: 134 against a baseline of 134
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
- Collected: 134 against a baseline of 134
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

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7393 against a baseline of 7393
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

### `r290-author.D2_parked_marked_resumable`

Mark a parked job's envelope resumable, which sends a wrapper to crate run for work only the verb can continue

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D2_parked_marked_resumable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7393 against a baseline of 7393
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome`

Old text:

```
            resumable=resumable,
            outcome=outcome,
```

New text:

```
            resumable=resumable or parked,
            outcome=outcome,
```

### `r290-author.D4_cancelled_reads_failed`

Read the cancelled type as the failed outcome, which is what the dispatcher said before Outcome.CANCELLED had a producer

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D4_cancelled_reads_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7393 against a baseline of 7393
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

### `r678-b.B1_emit_hands_in_no_drive`

the dispatcher never looks the drive up, so no queueing verb names its command

- File: `src/cratekit/cli/__init__.py`
- Source: `r678-b.json`, row `B1_emit_hands_in_no_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`
- Collected: 334 against a baseline of 334
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_favorites_names_the_job_and_the_command_that_drives_it`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`

Old text:

```
    print(render.render(envelope, drive=_drive_argv(envelope)), end="", file=stream)
```

New text:

```
    print(render.render(envelope), end="", file=stream)
```

### `r678-b.B2_drive_for_a_verb_that_did_not_queue`

job show and job resume name a second driver for a queued job

- File: `src/cratekit/cli/__init__.py`
- Source: `r678-b.json`, row `B2_drive_for_a_verb_that_did_not_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`
- Collected: 334 against a baseline of 334
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
- Collected: 334 against a baseline of 334
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
- Collected: 117 against a baseline of 117
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls`
  - `tests/test_provider_gate.py::test_calls_another_process_made_are_not_reported_as_this_runs`
  - `tests/test_provider_gate.py::test_rate_limit_answers_are_named_in_the_spend_line`
  - `tests/test_provider_gate.py::test_the_spend_line_reaches_a_person_on_the_human_output`
  - `tests/test_provider_gate.py::test_the_spend_line_survives_a_refusal`

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
- Collected: 117 against a baseline of 117
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls`
  - `tests/test_provider_gate.py::test_calls_another_process_made_are_not_reported_as_this_runs`
  - `tests/test_provider_gate.py::test_rate_limit_answers_are_named_in_the_spend_line`
  - `tests/test_provider_gate.py::test_the_spend_line_reaches_a_person_on_the_human_output`
  - `tests/test_provider_gate.py::test_the_spend_line_survives_a_refusal`

Old text:

```
    envelope = _with_provider_spend(envelope, spent_before)

```

New text:

```
    envelope = envelope

```

### `r924.D1_json_gets_progress`

The dispatcher hands the progress writer to JSON output too, so standard error carries progress under --output json

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D1_json_gets_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`

Old text:

```
        if not as_json:
            context.progress = _progress_to(stderr)
```

New text:

```
        if True:
            context.progress = _progress_to(stderr)
```

### `r924.D2_human_gets_none`

The dispatcher never hands a writer, so human output is silent again

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D2_human_gets_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 57 against a baseline of 57
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_human_fetch_runs_its_watcher`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
        if not as_json:
            context.progress = _progress_to(stderr)
```

New text:

```
        if False:
            context.progress = _progress_to(stderr)
```

### `r924.D3_write_failure_raises`

A progress line that cannot be written raises out of the paid pass

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D3_write_failure_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_closed_standard_error_does_not_end_a_paid_pass`

Old text:

```
        except (OSError, ValueError):
            pass
```

New text:

```
        except ValueError:
            pass
```

### `u168.C10_argv_never`

_dispatched: never record the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C10_argv_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1005 against a baseline of 1005
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
- Collected: 1005 against a baseline of 1005
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

### `u168.C9_argv_on_every_run`

_dispatched: record the command line on a continued run too, overwriting the first

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C9_argv_on_every_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1005 against a baseline of 1005
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`

Old text:

```
        if not args.run:
            state.argv = _verb_argv(argv, entry)
```

New text:

```
        if True:
            state.argv = _verb_argv(argv, entry)
```

### `u186.D1_dispatch_unhooked`

dispatcher: never call the sibling hook, so a second plan at its gate is told nothing

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D1_dispatch_unhooked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 9 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_reading_that_breaks_says_so_and_leaves_the_gate_as_it_was`
  - `tests/test_gate_siblings.py::test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor`
  - `tests/test_gate_siblings.py::test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run`
  - `tests/test_gate_siblings.py::test_a_sibling_whose_gate_is_open_is_named_as_open`
  - `tests/test_gate_siblings.py::test_an_answer_just_inside_twelve_hours_is_still_named`
  - `tests/test_gate_siblings.py::test_an_answer_ten_minutes_ago_is_named_with_its_actor_option_and_time`
  - `tests/test_gate_siblings.py::test_an_answer_with_no_recorded_time_is_named_as_unrecorded`
  - `tests/test_gate_siblings.py::test_one_warning_per_other_run`
  - `tests/test_gate_siblings.py::test_the_warning_prints_on_the_screen_a_person_reads`

Old text:

```
        if state is not None and resumable:
            envelope = _with_sibling_runs(envelope, state)
```

New text:

```
(empty)
```

### `u186.D2_dispatch_any_refusal`

dispatcher: call the hook on every refusal, not only a run persisted at its gate

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D2_dispatch_any_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_refusal_before_the_gate_names_no_sibling`

Old text:

```
        if state is not None and resumable:
            envelope = _with_sibling_runs(envelope, state)
```

New text:

```
        if state is not None:
            envelope = _with_sibling_runs(envelope, state)
```

### `u186.D3_dispatch_scope`

_with_sibling_runs: drop the database writing scope guard

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D3_dispatch_scope`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_verb_writing_no_database_says_nothing_of_its_own_siblings`

Old text:

```
    if not gates.writes_the_database(state.verb):
        return envelope
    try:
        found, unreadable = gates.siblings(state.verb, exclude=state.run_id)
```

New text:

```
    try:
        found, unreadable = gates.siblings(state.verb, exclude=state.run_id)
```

### `u186.D4_dispatch_break_silent`

_with_sibling_runs: a reading that breaks says nothing rather than naming the break

- File: `src/cratekit/cli/__init__.py`
- Source: `u186.json`, row `D4_dispatch_break_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_a_reading_that_breaks_says_so_and_leaves_the_gate_as_it_was`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - see the docstring, the gate stays the gate
        said = [
```

New text:

```
    except Exception as exc:  # noqa: BLE001 - see the docstring, the gate stays the gate
        said = [] and [
```

### `u193.M16_continue_job_branch`

continue_command: never resume the job, so a rerun queues a second job

- File: `src/cratekit/cli/__init__.py`
- Source: `u193.json`, row `M16_continue_job_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_label_playlists_releases.py`, `tests/test_label_playlists_kept.py`, `tests/test_config.py`, `tests/test_jobs.py`
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_for_a_job_resumes_that_job`

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
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`

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
- Collected: 508 against a baseline of 508
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`

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
- Collected: 508 against a baseline of 508
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
- Collected: 508 against a baseline of 508
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`

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
- Collected: 508 against a baseline of 508
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

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_second_run_over_the_same_set_asks_the_provider_no_isrc_again`
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

### `u210.R24_continue_run`

continue_command: never add the run a cause names

- File: `src/cratekit/cli/__init__.py`
- Source: `u210.json`, row `R24_continue_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_sync_pair_resume.py`
- Collected: 131 against a baseline of 131
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_continue_command_names_the_run_a_stopped_write_recorded_its_steps_under`

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
- Collected: 1180 against a baseline of 1180
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
- Collected: 1180 against a baseline of 1180
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
- Collected: 150 against a baseline of 150
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

### `u248.L10_built_before_the_builder`

build: count the verb built before its builder returns, so a builder that failed part way hands on a half built verb

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L10_built_before_the_builder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
            ) from exc
        self.built = True
```

New text:

```
            ) from exc
        self.built = self.built
```

### `u248.L1_lazy_off`

build_parser: build every verb eagerly whatever eager says, so every command imports every verb module again

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L1_lazy_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 12 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_lazy.py::test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working`
  - `tests/test_cli_lazy.py::test_a_defective_builder_is_a_defect_and_never_a_usage_error`
  - `tests/test_cli_lazy.py::test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra`
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb`
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`
  - `tests/test_cli_lazy.py::test_an_argument_error_raised_by_the_import_is_a_defect_too`
  - `tests/test_cli_lazy.py::test_doctor_help_loads_the_doctor_and_only_what_the_doctor_itself_imports`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[bare]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[help]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[version]`

Old text:

```
        if not eager:
            sub = target.add_parser(path[-1], help=entry.summary)
```

New text:

```
        if False:
            sub = target.add_parser(path[-1], help=entry.summary)
```

### `u248.L2_chosen_never_built`

_LazyChoices.__call__: never build the chosen verb, so it parses as an empty subparser with no handler

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L2_chosen_never_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 306 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_a_decision_naming_a_gate_the_verb_does_not_declare_is_refused`
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_contract.py::test_a_gate_is_answerable_from_a_different_process_in_a_later_session`
  - `tests/test_cli_contract.py::test_a_malformed_decision_is_refused_rather_than_ignored`
  - `tests/test_cli_contract.py::test_a_profile_that_switches_a_module_off_removes_its_verbs`
  - `tests/test_cli_contract.py::test_a_run_carrying_a_pending_action_reports_it_as_pending`
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_a_run_record_belongs_to_the_verb_that_created_it`
  - `tests/test_cli_contract.py::test_a_run_that_reached_a_gate_reports_it`
  - `tests/test_cli_contract.py::test_a_scripted_run_with_no_terminal_reaches_a_gate_and_exits_with_its_code`
  - `tests/test_cli_contract.py::test_a_verb_blocked_by_an_unverified_pending_action_refuses_before_doing_anything`
  - `tests/test_cli_contract.py::test_a_verb_that_exits_the_process_directly_is_converted_rather_than_obeyed`
  - `tests/test_cli_contract.py::test_a_verb_that_raises_something_unexpected_becomes_an_internal_cause`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - ... and 291 more, see the JSON sidecar

Old text:

```
        if waiting is not None:
            waiting.build()
```

New text:

```
        if waiting is not None:
            pass
```

### `u248.L3_listing_asks_everyone`

ask_for_listing: ask every verb, not only those declaring extras, so a group help imports all its verbs

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L3_listing_asks_everyone`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 4 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_group_help_loads_no_verb_module_when_none_of_its_verbs_declares_an_extra`
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[bare]`
  - `tests/test_cli_lazy.py::test_the_version_and_the_top_level_help_load_no_verb_module[help]`

Old text:

```
        if self.built or self.asked or not self.entry.extras_modules:
```

New text:

```
        if self.built or self.asked:
```

### `u248.L4_listing_drops_the_stub_line`

ask_for_listing: a missing extra no longer makes the stub, so the listing omits (requires the extra)

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L4_listing_drops_the_stub_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 1206 against a baseline of 1206
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

### `u248.L5_listing_asked_twice`

ask_for_listing: forget it was asked, so one help screen imports the module twice

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L5_listing_asked_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_listing_asks_only_the_verbs_whose_line_could_differ`
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
        self.asked = True
```

New text:

```
        self.asked = False
```

### `u248.L6_built_twice`

build: drop the built check, so a parser asked twice runs the builder twice and argparse refuses a duplicate option

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L6_built_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_verb_is_built_once_however_often_it_is_asked`

Old text:

```
        if self.built:
            return
        try:
            try:
                module = self.importer(self.entry.module)
```

New text:

```
        try:
            try:
                module = self.importer(self.entry.module)
```

### `u248.L7_defect_as_stub`

build: treat every import error as a missing extra, so a defect of our own reads as install the extra

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L7_defect_as_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_defect_in_our_own_module_does_not_masquerade_as_a_missing_extra`
  - `tests/test_cli_lazy.py::test_a_broken_module_fails_its_own_verb_and_leaves_every_other_one_working`

Old text:

```
                if not _is_missing_extra(exc, self.entry):
                    raise
                self._stub(exc)
                return
```

New text:

```
                self._stub(exc)
                return
```

### `u248.L8_listing_raises_a_defect`

ask_for_listing: let a non extra failure escape, so a broken module takes its whole group's help down

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L8_listing_raises_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 1 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_module_that_raises_anything_at_import_is_listed_plainly_and_raises_for_its_verb`

Old text:

```
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            pass
```

New text:

```
        except Exception:  # noqa: BLE001 - see the docstring, the verb itself raises
            raise
```

### `u248.L9_argument_error_unwrapped`

build: let an ArgumentError from the import or the builder reach argparse, so a defect of ours exits 2 as the user's usage error

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L9_argument_error_unwrapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`
- Collected: 1155 against a baseline of 1155
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_lazy.py::test_a_defective_builder_is_a_defect_and_never_a_usage_error`
  - `tests/test_cli_lazy.py::test_an_argument_error_raised_by_the_import_is_a_defect_too`

Old text:

```
        except argparse.ArgumentError as exc:
            raise RuntimeError(
```

New text:

```
        except ZeroDivisionError as exc:
            raise RuntimeError(
```

### `u274.I1_context_drops_warnings`

Context.run_job: return the drift warnings only, so the drive's warnings never reach the envelope

- File: `src/cratekit/cli/__init__.py`
- Source: `u274.json`, row `I1_context_drops_warnings`
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
        return result, (*handlers.drift_warnings(result.drifted), *result.warnings)

```

New text:

```
        return result, handlers.drift_warnings(result.drifted)

```

### `u278.M20_report_spends_reserve`

spends_reserve: a --report run spends the reserve

- File: `src/cratekit/cli/__init__.py`
- Source: `u278.json`, row `M20_report_spends_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_cli_contract.py`
- Collected: 1174 against a baseline of 1174
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
- Collected: 1174 against a baseline of 1174
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
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_calls_past_the_budget_is_refused_before_a_verb_that_makes_no_call_runs`
  - `tests/test_provider_budget.py::test_the_continue_a_parked_job_prints_is_not_refused_by_its_own_calls`

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
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1465 against a baseline of 1465
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
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1465 against a baseline of 1465
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
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1465 against a baseline of 1465
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
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1465 against a baseline of 1465
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

### `r345.B5_remote_into_document`

_resolve_backup: do not write the derived remote into the document, so the file carries no remote

- File: `src/cratekit/cli/setup.py`
- Source: `r345.json`, row `B5_remote_into_document`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1465 against a baseline of 1465
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
- Ran: `tests/test_doctor.py`, `tests/test_paths_resolved.py`, `tests/test_cli_contract.py`
- Collected: 1465 against a baseline of 1465
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
  - `tests/test_paths_resolved.py::test_setup_offers_the_root_when_rekordbox_still_records_the_old_name_twice`
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
        # THE COPY ITSELF, not the open.
```

New text:

```
    except ZeroDivisionError as exc:
        # THE COPY ITSELF, not the open.
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
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_root_sits_under_the_recorded_drive`
  - `tests/test_paths_resolved.py::test_setup_offers_nothing_when_the_two_drive_names_agree`

Old text:

```
    if root == base or root.startswith(base + "/"):
```

New text:

```
    if False:
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
- Ran: `tests/test_doctor.py`, `tests/test_cli_contract.py`
- Collected: 1414 against a baseline of 1414
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

### `r83.P3_empty_secret_note_status`

R-347: the wizard's empty credential note is FAIL instead of INFO

- File: `src/cratekit/cli/setup.py`
- Source: `r83.json`, row `P3_empty_secret_note_status`
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
                # whole wizard over a session blob only login can produce (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.INFO,
```

New text:

```
                # whole wizard over a session blob only login can produce (R-347).
                wizard.note(
                    f"setup.credential.{name}",
                    f"credential {name}",
                    doctor.Status.FAIL,
```

### `r83.P4_empty_secret_branch`

R-347: remove the NothingEntered branch so the unreadable branch catches it

- File: `src/cratekit/cli/setup.py`
- Source: `r83.json`, row `P4_empty_secret_branch`
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
                # An offer accepted and then left empty is the same fact as a
                # no: nothing recorded, doctor reports it. A FAIL here failed the
                # whole wizard over a session blob only login can produce (R-347).
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

### `u154.G16_wizard_default_dropped`

setup records no processed_dir when nothing answers

- File: `src/cratekit/cli/setup.py`
- Source: `u154.json`, row `G16_wizard_default_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_processed_dir.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_processed_dir.py::test_a_clean_machine_records_the_default_when_no_flag_names_one`

Old text:

```
            question="Which folder under the music folder holds filed batches",
            default=config.DEFAULT_PROCESSED_DIR,

```

New text:

```
            question="Which folder under the music folder holds filed batches",
            default="Filed_Elsewhere",

```

### `u27-round-8-independent.S1_act_always_generic`

_act stops asking render.access_note and always closes with the generic clause

- File: `src/cratekit/cli/setup.py`
- Source: `u27-round-8-independent.json`, row `S1_act_always_generic`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`
- Collected: 22933 against a baseline of 22933
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
- Collected: 22933 against a baseline of 22933
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
- Collected: 22933 against a baseline of 22933
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

### `u283.S10_any_raise_escapes`

_link_discogs: the bare except catches only arithmetic errors, so a check raising anything else escapes setup after the configuration is saved

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S10_any_raise_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 2 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_check_that_raises_anything_else_stores_nothing_and_is_a_note`
  - `tests/test_setup_discogs.py::test_an_exception_carrying_the_token_never_reaches_the_note`

Old text:

```
        except Exception as exc:  # noqa: BLE001
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"the token could not be checked ({type(exc).__name__}), so it was "
```

New text:

```
        except ArithmeticError as exc:  # noqa: BLE001
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"the token could not be checked ({type(exc).__name__}), so it was "
```

### `u283.S11_vocabulary_never_noted`

_discogs_vocabulary: never notes a copy without the Discogs table

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S11_vocabulary_never_noted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 2 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_copy_without_the_discogs_table_is_pointed_to_taxonomy_upgrade`
  - `tests/test_setup_discogs.py::test_an_already_linked_copy_without_the_table_is_pointed_there_too`

Old text:

```
    if searchers.DISCOGS not in found.missing_vocabularies:
        return
```

New text:

```
    if True:
        return
```

### `u283.S12_vocabulary_always_noted`

_discogs_vocabulary: notes every copy, the table present or not

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S12_vocabulary_always_noted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_copy_with_the_table_or_no_copy_gets_no_such_note`

Old text:

```
    if searchers.DISCOGS not in found.missing_vocabularies:
        return
```

New text:

```
    if False:
        return
```

### `u283.S13_linked_copy_not_checked`

_link_discogs: a token already recorded does not look at the copy's Discogs table

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S13_linked_copy_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_an_already_linked_copy_without_the_table_is_pointed_there_too`

Old text:

```
                f"as it is; crate setup {RELINK_FLAG} offers to replace it"
            ),
        )
        _discogs_vocabulary(wizard, cfg)
```

New text:

```
                f"as it is; crate setup {RELINK_FLAG} offers to replace it"
            ),
        )
```

### `u283.S14_no_explanation`

_link_discogs: the explanation is not written before the question

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S14_no_explanation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_the_step_explains_before_it_asks`

Old text:

```
    wizard.prompter.write(DISCOGS_INTRO)
```

New text:

```
    pass
```

### `u283.S15_nothing_entered_fails`

_link_discogs: an empty entry is a FAIL rather than the skip note

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S15_nothing_entered_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_setup_discogs.py::test_skipping_is_a_note_saying_what_it_costs_and_how_to_link_later[nothing-entered]`

Old text:

```
            wizard.note(key, title, doctor.Status.INFO, f"nothing was entered; {unlinked}")
```

New text:

```
            wizard.note(key, title, doctor.Status.FAIL, f"nothing was entered; {unlinked}")
```

### `u283.S16_refusal_line_leaks`

_link_discogs: the refusal line written to the terminal carries the token

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S16_refusal_line_leaks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 3 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_malformed_token_is_refused_without_a_request_and_asked_again`
  - `tests/test_setup_discogs.py::test_a_rejected_token_is_refused_offered_again_and_never_stored`
  - `tests/test_setup_discogs.py::test_the_verb_refuses_a_rejected_token_and_stores_nothing`

Old text:

```
            wizard.prompter.write(f"  Not linked: {check.note}. Nothing was recorded.\n")
```

New text:

```
            wizard.prompter.write(f"  Not linked: {check.note} {token}. Nothing was recorded.\n")
```

### `u283.S17_verb_skips_step`

setup: the verb no longer runs the Discogs step

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S17_verb_skips_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 4 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_the_verb_hands_the_flag_to_the_step`
  - `tests/test_setup_discogs.py::test_the_verb_links_discogs_through_the_shipped_client`
  - `tests/test_setup_discogs.py::test_the_verb_refuses_a_rejected_token_and_stores_nothing`
  - `tests/test_setup_discogs.py::test_the_verb_without_the_flag_leaves_a_recorded_token`

Old text:

```
    _link_discogs(wizard, cfg, relink=bool(args.relink_discogs))
```

New text:

```
    pass
```

### `u283.S1_loop_offers_discogs_again`

_capture_credentials: drop the pass over the Discogs check, so the bare loop offers and stores the token unchecked beside the step

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S1_loop_offers_discogs_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 3 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_wizard_offers_every_credential_the_profile_needs_and_records_it`
  - `tests/test_doctor.py::test_the_wizard_reports_no_check_key_twice`
  - `tests/test_setup_discogs.py::test_the_credential_loop_no_longer_offers_discogs`

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

### `u283.S2_step_ignores_offered`

_link_discogs: drop the doctor offered question, so a profile whose verbs spend no token is asked anyway

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S2_step_ignores_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_profile_whose_verbs_spend_no_token_is_not_offered_discogs`

Old text:

```
    if not doctor.offered(DISCOGS_CHECK, membership):
        return
    name = str(secrets.Credential.DISCOGS_TOKEN)
```

New text:

```
    if False:
        return
    name = str(secrets.Credential.DISCOGS_TOKEN)
```

### `u283.S3_relink_flag_ignored`

_link_discogs: a recorded token is acknowledged even with --relink-discogs, so the flag replaces nothing

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S3_relink_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 7 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_declined_relink_keeps_the_recorded_token`
  - `tests/test_setup_discogs.py::test_a_refused_replacement_keeps_the_recorded_token`
  - `tests/test_setup_discogs.py::test_a_replacement_discogs_could_not_check_keeps_the_recorded_token[blocked]`
  - `tests/test_setup_discogs.py::test_a_replacement_discogs_could_not_check_keeps_the_recorded_token[outage]`
  - `tests/test_setup_discogs.py::test_a_replacement_discogs_could_not_check_keeps_the_recorded_token[transport]`
  - `tests/test_setup_discogs.py::test_relinking_replaces_the_recorded_token_once_discogs_accepts_the_new_one`
  - `tests/test_setup_discogs.py::test_the_verb_hands_the_flag_to_the_step`

Old text:

```
    if already and not relink:
```

New text:

```
    if already:
```

### `u283.S4_recorded_never_acknowledged`

_link_discogs: a recorded token is not acknowledged, so every run asks for it again and may replace it

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S4_recorded_never_acknowledged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 3 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_recorded_token_is_acknowledged_with_no_question_and_no_request`
  - `tests/test_setup_discogs.py::test_an_already_linked_copy_without_the_table_is_pointed_there_too`
  - `tests/test_setup_discogs.py::test_the_verb_without_the_flag_leaves_a_recorded_token`

Old text:

```
    if already and not relink:
```

New text:

```
    if False:
```

### `u283.S5_rejected_falls_through_to_store`

_link_discogs: a token Discogs rejected is not asked again but falls through to the store

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S5_rejected_falls_through_to_store`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 4 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_malformed_token_is_refused_without_a_request_and_asked_again`
  - `tests/test_setup_discogs.py::test_a_rejected_token_is_refused_offered_again_and_never_stored`
  - `tests/test_setup_discogs.py::test_every_try_rejected_stores_nothing_and_is_a_note_not_a_failure`
  - `tests/test_setup_discogs.py::test_the_verb_refuses_a_rejected_token_and_stores_nothing`

Old text:

```
            wizard.prompter.write(f"  Not linked: {check.note}. Nothing was recorded.\n")
            continue
```

New text:

```
            wizard.prompter.write(f"  Not linked: {check.note}. Nothing was recorded.\n")
```

### `u283.S6_relink_stores_unchecked`

_link_discogs: drop the round one guard, so a replacement Discogs could not check overwrites the recorded token

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S6_relink_stores_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 3 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_replacement_discogs_could_not_check_keeps_the_recorded_token[blocked]`
  - `tests/test_setup_discogs.py::test_a_replacement_discogs_could_not_check_keeps_the_recorded_token[outage]`
  - `tests/test_setup_discogs.py::test_a_replacement_discogs_could_not_check_keeps_the_recorded_token[transport]`

Old text:

```
        if already and check.verdict is not searchers.TokenVerdict.ACCEPTED:
```

New text:

```
        if False:
```

### `u283.S7_accepted_note_swapped`

_link_discogs: an accepted token is noted as unchecked and an unchecked one as accepted

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S7_accepted_note_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 8 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_discogs_that_could_not_be_asked_stores_the_token_with_a_note[blocked]`
  - `tests/test_setup_discogs.py::test_a_discogs_that_could_not_be_asked_stores_the_token_with_a_note[not-the-api]`
  - `tests/test_setup_discogs.py::test_a_discogs_that_could_not_be_asked_stores_the_token_with_a_note[outage]`
  - `tests/test_setup_discogs.py::test_a_discogs_that_could_not_be_asked_stores_the_token_with_a_note[transport]`
  - `tests/test_setup_discogs.py::test_a_rejected_token_is_refused_offered_again_and_never_stored`
  - `tests/test_setup_discogs.py::test_a_valid_token_is_checked_and_then_stored_where_login_stores_it`
  - `tests/test_setup_discogs.py::test_relinking_replaces_the_recorded_token_once_discogs_accepts_the_new_one`
  - `tests/test_setup_discogs.py::test_the_verb_links_discogs_through_the_shipped_client`

Old text:

```
        if check.verdict is searchers.TokenVerdict.ACCEPTED:
            wizard.note(
```

New text:

```
        if check.verdict is not searchers.TokenVerdict.ACCEPTED:
            wizard.note(
```

### `u283.S8_more_tries`

DISCOGS_TRIES: five tries rather than the prompter's three

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S8_more_tries`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_every_try_rejected_stores_nothing_and_is_a_note_not_a_failure`

Old text:

```
DISCOGS_TRIES = prompt.MAX_ATTEMPTS
```

New text:

```
DISCOGS_TRIES = 5
```

### `u283.S9_default_no`

_link_discogs: the question defaults to no, so pressing return skips linking

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S9_default_no`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_the_step_explains_before_it_asks`

Old text:

```
    if not wizard.optional(question, default=True):
```

New text:

```
    if not wizard.optional(question, default=False):
```

### `r1115.S1_sync_land_stops_on_unsettled`

sync land _download: carry on over a download that did not settle, so a transient failure lands the rest

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1115.json`, row `S1_sync_land_stops_on_unsettled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_crate_sync_skill.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_parked_download_ends_the_pass_blocked_before_the_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
    if not read.settled:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
```

New text:

```
    if False:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
```

### `r1115.S2_sync_land_names_the_refused`

sync land _download: report no refused track

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1115.json`, row `S2_sync_land_names_the_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_crate_sync_skill.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
    refused = [dict(row) for row in read.refused]
```

New text:

```
    refused = []
```

### `r1499.S01_download_reading`

sync land: the reading before the download never refuses, so a pass downloads beside a go's download at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S01_download_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`
  - `tests/test_sync_land_beside.py::test_a_label_gos_download_at_its_landings_gate_renamed_refuses_the_pass_before_it_downloads`
  - `tests/test_sync_land_beside.py::test_a_pass_whose_landing_is_proven_is_not_named`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == DOWNLOAD:
        return settled

```

### `r1499.S02_tail_reading`

sync land: the reading before the tail never refuses, so a download finished during the pass's download is tailed and landed with it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S02_tail_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_gos_download_arriving_while_the_pass_downloads_refuses_its_tail`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == TAG:
        return settled

```

### `r1499.S03_arrival_after_tail`

sync land: no check after name apply, so a download finished during the tail is renamed and planned into the landing

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S03_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
            if changed is not None:
                # NOT CONTINUED
```

New text:

```
            if False:
                # NOT CONTINUED
```

### `r1499.S04_arrival_after_plan`

sync land: a landing planned over an arrival is handed on at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S04_arrival_after_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`

Old text:

```
                changed = _arrived(cfg, staging, name, before)
                if changed is None:
                    raise

```

New text:

```
                changed = None
                if changed is None:
                    raise

```

### `r1499.S05_keep_after_arrival`

_keep: keep the record although something arrived, so the arrival reads as the pass's own on its next run

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S05_keep_after_arrival`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if why is not None:
        report.warnings.append(
```

New text:

```
    if False:
        report.warnings.append(
```

### `r1499.S06_keep_called`

sync land: keep no record at the tail's stop, so the pass continued refuses beside its own renamed tracks

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S06_keep_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`
  - `tests/test_sync_land_beside.py::test_the_record_is_kept_under_the_pass_at_each_tail_stop`

Old text:

```
            _keep(report, cfg, staging, name, before)
```

New text:

```
            pass
```

### `r1499.S07_kept_read`

_alone: read no kept record, so the pass's own renamed tracks are beside it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S07_kept_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`

Old text:

```
                kept=staged.kept(staged.pass_record(cfg, name)),
```

New text:

```
                kept=frozenset(),
```

### `r1499.S08_own_pass_proof`

_alone: never read the pass's landing proof, so a landed pass's record still reads files as its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S08_own_pass_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`

Old text:

```
                own_pass=name,
                origin=_ORIGIN,
```

New text:

```
                own_pass=None,
                origin=_ORIGIN,
```

### `r1499.S09_own_library`

_own_downloads: a download of another library over the pass's list is its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S09_own_library`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name`

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name
```

### `r1499.S10_own_by_list`

_own_downloads: no download is the pass's own, so its own fresh tracks refuse it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S10_own_by_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 66 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_job_command_that_stops_at_a_gate_is_that_commands_gate`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - ... and 51 more, see the JSON sidecar

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name + '-' and job.library_id == cfg.library.volume_id
```

### `r1499.S11_unreadable_refuses`

_alone: a refusal of the reading (an unlistable folder, an unreadable root) reads as nothing beside

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S11_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`

Old text:

```
    except CratekitError as exc:
        raise _Stop(step, exc) from None
    except OSError
```

New text:

```
    except CratekitError:
        return staged.Settled(frozenset(), 0)
    except OSError
```

### `r1499.S12_warnings_in_refusal`

_with_warnings: a refusal drops the pass's warnings

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S12_warnings_in_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if report.warnings:
        data["warnings"]
```

New text:

```
    if False:
        data["warnings"]
```

### `r1499.S13_own_unnamed_step`

_own_unnamed: never name the landing under the pass for files no download names

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S13_own_unnamed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`

Old text:

```
    if not (found.unnamed and own):
        return ()
```

New text:

```
    if True:
        return ()
```

### `u152.R13_missing_lift`

_missing: carry none of the listing's failing rows

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R13_missing_lift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`

Old text:

```
    # cannot name exactly above all: it is in no download list, and the pass
    # would otherwise say nothing of it.
    _lift_failed_checks(report, envelope)

```

New text:

```
    # cannot name exactly above all: it is in no download list, and the pass
    # would otherwise say nothing of it.

```

### `u152.R14_download_list_match`

_download_job: drop the list match, so another list's download job is read as the pass's

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R14_download_list_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`

Old text:

```
            and str((job.payload or {}).get(acquire_cli.LIST) or "") == wanted

```

New text:

```
(empty)
```

### `u152.R15_download_newest`

_download_job: read the oldest job over the list, the round two defect

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R15_download_newest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
    for job in jobs.list_jobs(store):
        if (
            job.handler_key == key
```

New text:

```
    for job in reversed(jobs.list_jobs(store)):
        if (
            job.handler_key == key
```

### `u152.R16_download_cancelled`

_download_job: read a cancelled download as the pass's claim on the list

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R16_download_cancelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`

Old text:

```
            and job.state is not jobs.JobState.CANCELLED

```

New text:

```
(empty)
```

### `u152.R17_download_retry`

_download: never retry a download that failed transiently, so a continued pass reads it as settled

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R17_download_retry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`

Old text:

```
            job = jobs.retry(store, job.job_id)
```

New text:

```
            pass
```

### `u152.R20_nothing_downloaded`

_download: go on to the tail when the download landed nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R20_nothing_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
    if not done:
        report.check(
```

New text:

```
    if False:
        report.check(
```

### `u152.R2_preflight_backup`

_preflight: drop the backup driver check, so a pass runs beside a live backup

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R2_preflight_backup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_running_backup_refuses_before_any_write`

Old text:

```
        try:
            jobs.assert_free(job.job_id)
        except jobs.DriverHeld as exc:
```

New text:

```
        try:
            pass
        except jobs.DriverHeld as exc:
```

### `u152.R6_lift_failed_checks`

_lift_failed_checks: carry no step's failing row, so the withheld hearts and the unnameable tracks are said nowhere

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R6_lift_failed_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
        if check.get("key") in held:
            continue
        report.checks.append(dict(check))
```

New text:

```
        if check.get("key") in held:
            continue
```

### `u152.R7_outbound_held`

_lift_failed_checks: lift the unasked outbound write's refusal as a FAIL row on every pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R7_outbound_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`
  - `tests/test_sync_land.py::test_the_outbound_hearts_write_stays_behind_its_own_gate`

Old text:

```
        if check.get("key") in held:
            continue

```

New text:

```
(empty)
```

### `u152.R8_continue_open_pass`

_sync: never continue the one earlier pass sync all left out, so a hand typed pass ends no_op

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R8_continue_open_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`

Old text:

```
        if len(earlier) == 1:
```

New text:

```
        if False:
```

### `u152.R9_open_passes_library`

_open_intake: drop the library filter, so another library's open pass is continued

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R9_open_passes_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1183 against a baseline of 1183
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_that_ended_or_belongs_to_another_library_is_not_continued`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
            and job.library_id == cfg.library.volume_id
        ]


def _run_of
```

New text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
        ]


def _run_of
```

### `u179.P1_shared_preflight`

preflight: drop the rekordbox check, so sync bandcamp plans and fetches with rekordbox open

- File: `src/cratekit/cli/sync_land.py`
- Source: `u179.json`, row `P1_shared_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`
- Collected: 104 against a baseline of 104
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_rekordbox_running_refuses_before_the_plan`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_rekordbox_running_refuses_before_any_write`

Old text:

```
    rb_writer.assert_rekordbox_closed(verb)
```

New text:

```
    pass
```

### `u181.S1_profile_off_asked`

sync land _vocals: ask the model on a profile with the vocals module off

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S1_profile_off_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`

Old text:

```
    if not tail.vocals_on(cfg):
        report.summary["vocal_scoring"] = "off"
```

New text:

```
    if False:
        report.summary["vocal_scoring"] = "off"
```

### `u181.S2_gate_never_asked`

sync land _vocals: never stop at the gate, so a pass lands rows with no score unasked

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S2_gate_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 6 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.land]`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_cannot_score_stops_at_its_gate_before_queueing_anything`
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_gate_recorded_by_a_separate_act_continues_the_same_run`

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

### `u181.S3_stop_goes_on`

sync land _vocals: an answer of stop takes the pass on

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S3_stop_goes_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`

Old text:

```
    if option != WITHOUT_VOCALS_GO:
```

New text:

```
    if option is None:
```

### `u182.M18_left_open_taken`

_left_behind: name the pass's own jobs on the left open row too

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M18_left_open_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
    left = [hold for hold in holds if not taken or _run_of(hold.job) != taken]
```

New text:

```
    left = list(holds)
```

### `u182.M19_left_open_identity`

_left_behind: group by the label alone, so a typed URL and a sweep's id are two playlists

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M19_left_open_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        grouped.setdefault(hold.identity or hold.label(), []).append(hold)
```

New text:

```
        grouped.setdefault(hold.label(), []).append(hold)
```

### `u182.M20_cancelled_driven`

_intake: drive cancelled jobs with the rest, so a continued pass stops on a cancelled job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M20_cancelled_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
    live = [job for job in found if job.state is not jobs.JobState.CANCELLED]
```

New text:

```
    live = list(found)
```

### `u182.M21_all_cancelled_done`

_intake: go on when every job was cancelled, so the listing refuses a pass with nothing resolved

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M21_all_cancelled_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
        if not live:
            report.check(
```

New text:

```
        if False:
            report.check(
```

### `u182.M22_skip_failed`

_missing: list without --skip-failed, so a pass with a cancelled copy stops at the listing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M22_skip_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`

Old text:

```
        argv.append("--skip-failed")
```

New text:

```
        pass
```

### `u183.M11_land_runs_named`

_unknown_pass: name no land run beside a recent pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M11_land_runs_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    lands = _land_runs_of(passes)
```

New text:

```
    lands: dict[str, str] = {}
```

### `u183.M12_preflight_way_back`

_preflight: a rekordbox or backup refusal no longer ends with the command that comes back

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M12_preflight_way_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`

Old text:

```
        raise tail.with_steps(exc, f"then run it again: {again}") from None
```

New text:

```
        raise
```

### `u183.M14_retryable_intake_continues`

_intake: a retryable ended intake job stops as one that cannot continue, so its way on ends at the resume

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M14_retryable_intake_continues`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`

Old text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry))
```

New text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry), continues=False)
```

### `u183.M15_continue_command_words`

_continue_command: drop the flag, so every printed continuation starts a new pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M15_continue_command_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_an_unknown_id_refuses_before_any_step_and_names_the_recent_passes`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_two_earlier_passes_holding_open_jobs_are_a_choice_named_not_made`

Old text:

```
    return f"crate sync land --pass-run {pass_run}"
```

New text:

```
    return f"crate sync land {pass_run}"
```

### `u183.M1_pass_run_as_given`

_resolve: never take the given id as a pass run, so a pass id is looked up as a land record and refused

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M1_pass_run_as_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`
  - `tests/test_sync_land.py::test_a_job_another_driver_holds_ends_the_pass_with_that_drivers_refusal`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_failed_names_its_retry_not_a_continuation`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_left_open_row_names_each_playlist_its_age_size_and_copies`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if _pass_jobs(store, given, cfg):
            return given
```

New text:

```
        if False:
            return given
```

### `u183.M2_land_record_resolves`

_resolve: ignore the land run's recorded pass, so the land run's own id is refused as it was before U183

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M2_land_record_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if recorded:
```

New text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if False:
```

### `u183.M3_recorded_pass_needs_a_job`

_resolve: take a land run's recorded pass with no intake job of this library, so the pass fails at the fourth step again

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M3_recorded_pass_needs_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_land_run_whose_pass_no_intake_job_carries_is_refused_not_continued`

Old text:

```
            if _pass_jobs(store, recorded, cfg):
                report.check(
```

New text:

```
            if True:
                report.check(
```

### `u183.M6_unreadable_record`

_land_record: let a record that cannot be read raise out of the resolver

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M6_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    except (CratekitError, AttributeError, KeyError, TypeError, ValueError, OSError):
        return None
    return state if
```

New text:

```
    except KeyError:
        return None
    return state if
```

### `u183.M7_remember_saves`

_remember: record the pass on the run without saving, so a run that stops before the dispatcher saves keeps nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M7_remember_saves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
    gates.save(ctx.run)
```

New text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
```

### `u183.M8_remember_called`

sync_land: never record the pass on the land run

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M8_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
        if run_id:
            _remember(ctx, report, run_id)
```

New text:

```
        if False:
            _remember(ctx, report, run_id)
```

### `u212.S1_missing_ends`

sync_land._missing: nothing listed ends the pass whatever is staged

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S1_missing_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`

Old text:

```
    if (envelope.get("outcome") == str(Outcome.NO_OP) or not listed) and not staged:
```

New text:

```
    if envelope.get("outcome") == str(Outcome.NO_OP) or not listed:
```

### `u212.S2_download_refused_all`

sync_land._download: a download that landed nothing ends the pass whatever is staged, round one's F1

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S2_download_refused_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not listed.staged:
            raise _Done(DOWNLOAD)
        return 0
    report.check(
```

New text:

```
        raise _Done(DOWNLOAD)
    report.check(
```

### `u212.S3_no_list_download`

sync_land._download: no early return for a pass with no list, so it asks the download verb for a list that is not there

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S3_no_list_download`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if listed.path is None:
        report.check(DOWNLOAD, "info", "nothing downloaded: every missing track is staged already")
        return 0
```

New text:

```
(empty)
```

### `u212.S4_staged_said`

sync_land._missing: the missing row drops the staged clause, so the pass does not say how many it skipped

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S4_staged_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 334 against a baseline of 334
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        + (f"; {staged} more {held}" if staged else ""),
```

New text:

```
        + "",
```

### `u227.R15_way_on_wording`

_way_on: name a mirror download as queued by hand, to be driven outside a pass (round one's S12)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R15_way_on_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif False:
```

### `u227.R19_take_library`

_take_mirror_downloads: take another library's mirror job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R19_take_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_another_library_queued_is_not_taken`

Old text:

```
                or job.library_id != cfg.library.volume_id

```

New text:

```
(empty)
```

### `u227.R20_take_source`

_mirror_download: any intake.playlist job is a mirror download, a hand queued one included

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R20_take_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_queued_by_hand_with_no_pass_is_named_not_passed_over`
  - `tests/test_sync_land_mirror_downloads.py::test_a_hand_queued_playlist_job_and_a_cancelled_mirror_job_are_not_taken`

Old text:

```
        and (job.payload or {}).get("source_id") == mirror_downloads.SOURCE_ID

```

New text:

```
(empty)
```

### `u227.R21_take_continued`

sync_land: take mirror jobs into a continued earlier pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R21_take_continued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none`

Old text:

```
            if fresh and run_id in (None, fresh) and _take_mirror_downloads(report, cfg, fresh):
```

New text:

```
            if fresh and _take_mirror_downloads(report, cfg, run_id or fresh):
```

### `u227.R22_take_not_driven`

sync_land: give the jobs the run but keep driving the pass sync all named nothing for

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R22_take_not_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_whose_sync_all_queued_nothing_takes_the_mirror_download`

Old text:

```
                run_id = fresh
                report.summary["pass_run"] = fresh
```

New text:

```
                pass
```

### `u227.R25_way_on_state`

_way_on: name a blocked mirror download as the next pass's, which takes queued jobs only (round two's R3)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R25_way_on_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_a_pass_cannot_take_keeps_the_command_that_settles_it`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif _mirror_download(job):
```

### `u293.S3_sync_land_holds`

sync_land: a pass by hand takes no staging lock

- File: `src/cratekit/cli/sync_land.py`
- Source: `u293.json`, row `S3_sync_land_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`

Old text:

```
    with staging_lock.held("crate sync land", run_id=ctx.run.run_id):
```

New text:

```
    if True:
```

### `u293.N1_no_answer`

_no_answer: an answer or a raised line given to the night is taken

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N1_no_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv0]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv1]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv2]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv3]`

Old text:

```
    if given:
```

New text:

```
    if False:
```

### `u293.N2_rekordbox_refused`

sync_night: the night runs beside rekordbox or its agent

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N2_rekordbox_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_night_writes_its_record_even_when_its_line_cannot_be_kept`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running0]`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running1]`

Old text:

```
            rb_writer.assert_rekordbox_closed("crate sync night")
```

New text:

```
            pass
```

### `u293.N3_live_job_refused`

sync_night: the night runs beside a job with a live driver

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N3_live_job_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_job_with_a_live_driver_refuses_before_any_call`

Old text:

```
            _no_live_job()
            pass_run
```

New text:

```
            pass_run
```

### `u293.N4_occupied_refused`

sync_night: a new pass runs beside what the staging folder holds

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N4_occupied_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_staging_folder_holding_what_a_landing_takes_refuses_a_new_pass`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
                _nothing_waits(cfg, last)
```

New text:

```
                pass
```

### `u293.N5_owed_kept`

_refused: a refusal writes a fresh record over a pass still owed

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N5_owed_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_the_next_night_continues`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
    if _owed(last) and last is not None:
```

New text:

```
    if False:
```

### `u293.N6_settled_by_landing`

settle: the pass's own landing never ends a wait, so a landed pass reads as waiting

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N6_settled_by_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`

Old text:

```
    if _landed(cfg, record.get("land_name")):
```

New text:

```
    if False:
```

### `u293.N7_unread_landing_is_not_settled`

_landed: a landing log that cannot be read is read as landed, so a waiting pass reads settled

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N7_unread_landing_is_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1068 against a baseline of 1068
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landing_that_cannot_be_read_settles_nothing`

Old text:

```
    except (CratekitError, OSError):
        return None
```

New text:

```
    except (CratekitError, OSError):
        return True
```

