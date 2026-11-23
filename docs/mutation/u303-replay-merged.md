# Mutation table: u303-replay-merged

Measured by `scripts/mutate.py` on 2026-11-23 04:23 UTC, branch `cloud/860-cli-fifth-smaller` at `547f7493`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22474 collected. pytest invocations for this batch: 132.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `e052c26fb862`, and this tree is at `547f74938868`).

Subset baselines: 39, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `docs/mutation/u303-replay-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22474 against 22474. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r239-b.S5_converge_key_off` | `src/cratekit/cli/converge.py` | user | 7 file(s) | 723 | 2 | killed |
| `r1255.D1_doctor_branches_on_the_scan` | `src/cratekit/cli/doctor_state.py` | user | 2 file(s) | 432 | 1 | killed |
| `r787.D1_doctor_own_list` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2209 | 4 | killed |
| `r787.D2_set_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2209 | 1 | killed |
| `r787.D3_source_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2209 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2209 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2209 | 1 | killed |
| `u206.M24_doctor_set_aside_unnamed` | `src/cratekit/cli/doctor_state.py` | user | 9 file(s) | 1118 | 1 | killed |
| `r388-b.M12_listing_steps_say_take_a_backup` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 684 | 2 | killed |
| `r388-c.M13_credential_step_dropped` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 684 | 2 | killed |
| `r388-d.M16_named_stamp_step_dropped_remeasured` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 684 | 2 | killed |
| `u72.M8_registry_digest_source` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 27 | 7 | killed |
| `r679-a.E1_cli_offers_every_verdict` | `src/cratekit/cli/review.py` | user | 3 file(s) | 833 | 1 | killed |
| `r679-a.E2_listing_drops_the_actor` | `src/cratekit/cli/review.py` | user | 3 file(s) | 833 | 1 | killed |
| `r185-r246-author.D2_cloud_gate_restored` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5846 | 2 | killed |
| `r312.R1_summary_promises_a_replace` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5846 | 1 | killed |
| `r770-d.C8_native_gate_answered_inline` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1031 | 6 | killed |
| `u103-b.M1_identify_declared_adjudicating` | `src/cratekit/cli/registry.py` | maintainer | 2 file(s) | 1064 | collection error | collect-error |
| `u129-author.A10_export_set_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 20 | 1 | killed |
| `u129-author.A11_export_archive_without_library_mounted` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 20 | 1 | killed |
| `u129-author.A9_land_without_provider_check` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 20 | 1 | killed |
| `u27-reports-round-1.R1_delete_review_precondition` | `src/cratekit/cli/registry.py` | user | 14 file(s) | 3877 | 2 | killed |
| `u39-author-full.W2_unreachable_gate_restored` | `src/cratekit/cli/registry.py` | user | 19 file(s) | 4044 | 1 | killed |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry.py` | maintainer | 21 file(s) | 4176 | collection error | collect-error |
| `u44-author.D1_registry_drops_long_running` | `src/cratekit/cli/registry.py` | maintainer | 22 file(s) | 4252 | collection error | collect-error |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4372 | collection error | collect-error |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4375 | collection error | collect-error |
| `u69-b.M20_registry_schema` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1038 | 24 | killed |
| `u161.G1_pin_never_compared` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 66 | 4 | killed |
| `u161.G2_pin_overwritten_before_compare` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 66 | 3 | killed |
| `u161.G3_absence_read_as_agreement` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 66 | 2 | killed |
| `u161.G4_pins_not_written` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 66 | 24 | killed |
| `u161.G5_pins_not_read` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 66 | 24 | killed |
| `u49-author.G2_the_second_raise_site_drops_the_context` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1992 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 359 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 359 | 21 | killed |
| `u58-workers-and-wav.H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 8 file(s) | 613 | 33 | killed |
| `r678-a.A10_proof_ungated_on_verb` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 1 | killed |
| `r678-a.A11_run_count_not_the_total` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 1 | killed |
| `r678-a.A12_retired_file_unnamed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 3 | killed |
| `r678-a.A1_drop_the_job_state_case` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 9 | killed |
| `r678-a.A2_drop_the_import_proof_case` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 2 | killed |
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
| `r925.R3_no_isrc_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 2 | killed |
| `r925.R4_version_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `r925.R6_count_line` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 2 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7236 | 47 | killed |
| `r290-author.D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7236 | 2 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7236 | 22 | killed |
| `r678-b.B1_emit_hands_in_no_drive` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 293 | 3 | killed |
| `r678-b.B2_drive_for_a_verb_that_did_not_queue` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 293 | 1 | killed |
| `r678-b.B3_narrow_catch` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 293 | 1 | killed |
| `r924.D1_json_gets_progress` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 52 | 1 | killed |
| `r924.D2_human_gets_none` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 52 | 5 | killed |
| `r924.D3_write_failure_raises` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 11 | 1 | killed |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 9 file(s) | 1118 | 3 | killed |
| `u248.L4_listing_drops_the_stub_line` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1207 | 4 | killed |
| `u212.S1_missing_ends` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 318 | 1 | killed |
| `u212.S4_staged_said` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 318 | 1 | killed |
| `r925.J2_playlist_excluded` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 4 | killed |
| `r925.J3_field_not_set` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 5 | killed |
| `r925.J4_isrc_dropped` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 2 | killed |
| `r925.J5_version_dropped` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 1 | killed |
| `u182.M17_summary_playlist` | `src/cratekit/cli/jobs.py` | user | 3 file(s) | 206 | 3 | killed |
| `u172-b.C3_left_miscounted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 1 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u172.C2_guess_without_pass` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 2 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 4 | killed |
| `u181.T2_rescore_ignores_profile` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 30 | killed |
| `u181.T3_rescore_keeps_stale` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u181.T4_rescore_failure_ignored` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u212.T1_reason_guard` | `src/cratekit/cli/tail.py` | maintainer | 11 file(s) | 1608 | 1 | killed |
| `u212.T2_done_only` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1608 | 1 | killed |
| `u212.T3_library` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1608 | 1 | killed |
| `u212.T4_earliest_first` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1608 | 1 | killed |
| `u212.T5_name_wraps` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1608 | 2 | killed |
| `u284.T1_pass_names_nothing` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u284.T2_pass_stop_unsaid` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u319.M10_sync_stop_drops_the_short_path` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 181 | 1 | killed |

## Row definitions

### `r239-b.S5_converge_key_off`

converge passes unlock=False again, so every native tree reads not compared on a real library

- File: `src/cratekit/cli/converge.py`
- Source: `r239-b.json`, row `S5_converge_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 723 against a baseline of 723
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

### `r1255.D1_doctor_branches_on_the_scan`

doctor _check_unresolved_session: never branch on the listing, so the log directory is named as an unreadable record

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r1255.json`, row `D1_doctor_branches_on_the_scan`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_doctor.py`, `tests/test_session_log_unlisted.py`
- Collected: 432 against a baseline of 432
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`

Old text:

```
    if session.log_unlisted(unreadable, inputs.cfg):
        unreadable_directory = session.log_dir(inputs.cfg)
```

New text:

```
    if False:
        unreadable_directory = session.log_dir(inputs.cfg)
```

### `r787.D1_doctor_own_list`

doctor's _declared_trees keeps a list of its own, the routing tree alone, instead of asking cutover_trees

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D1_doctor_own_list`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2209 against a baseline of 2209
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_and_the_verb_read_one_set_of_cutover_trees`
  - `tests/test_cutover_cli.py::test_doctor_fails_on_a_native_record_the_cutover_would_refuse_to_create`
  - `tests/test_cutover_cli.py::test_doctor_reads_a_native_inbox_record_as_ok`
  - `tests/test_cutover_cli.py::test_doctor_reads_an_inbox_the_verb_cut_over_as_ok`

Old text:

```
    return tuple(named), tree_registry.cutover_trees(declared), None
```

New text:

```
    return tuple(named), frozenset({declared.tree.id}), None
```

### `r787.D2_set_guard_removed`

doctor stops judging a native record by the set, so a native catalogue tree reads ok

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D2_set_guard_removed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2209 against a baseline of 2209
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_lists_and_fails_a_recorded_tree_the_taxonomy_does_not_declare`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            record.source not in tree_registry.REBUILDABLE
```

### `r787.D3_source_guard_removed`

doctor stops judging a native record by its source, so a native inbox from a catalogue crawl reads ok

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D3_source_guard_removed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2209 against a baseline of 2209
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_doctor_fails_a_native_inbox_whose_source_no_rebuild_reproduces`

Old text:

```
            tree_id not in may_cut_over or record.source not in tree_registry.REBUILDABLE
```

New text:

```
            tree_id not in may_cut_over
```

### `u132.D1_doctor_behind`

Doctor reads a copy behind the shipped schema as OK

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D1_doctor_behind`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2209 against a baseline of 2209
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_current_copy_with_every_entry_is_ok`
  - `tests/test_doctor.py::test_a_version_2_copy_without_favorites_is_named_with_both_versions`

Old text:

```
    if not found.behind:

```

New text:

```
    if found.behind:

```

### `u132.D2_doctor_defect`

Doctor reports a shipped template defect as the copy not compared

- File: `src/cratekit/cli/doctor_library.py`
- Source: `u132.json`, row `D2_doctor_defect`
- Moved: the same text, now in src/cratekit/cli/doctor_library.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2209 against a baseline of 2209
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_shipped_template_that_does_not_load_is_a_defect_and_not_the_copy`

Old text:

```
        if exc.cause.reason == "internal-error":

```

New text:

```
        if False:

```

### `u206.M24_doctor_set_aside_unnamed`

_check_isrc_cache: leave the set aside files out of the note

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u206.json`, row `M24_doctor_set_aside_unnamed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1118 against a baseline of 1118
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
    aside = cache.set_aside()
    if aside:
```

New text:

```
    aside = cache.set_aside()
    if False:
```

### `r388-b.M12_listing_steps_say_take_a_backup`

Replace the listing failure's first reserved step with the take a backup step it replaced

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-b.json`, row `M12_listing_steps_say_take_a_backup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 684 against a baseline of 684
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
            "check the backup remote is reachable from this machine; the snapshot "
            "is not known to be missing, a listing of it failed",
```

New text:

```
            "no dated database snapshot exists for this library yet; take a "
            "backup before a restore can be planned",
```

### `r388-c.M13_credential_step_dropped`

Drop the credential step from the listing failure's reservation

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-c.json`, row `M13_credential_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 684 against a baseline of 684
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
            "check the remote's credential has not expired or been revoked, and "
            "reconnect it in rclone if it has",

```

New text:

```
(empty)
```

### `r388-d.M16_named_stamp_step_dropped_remeasured`

Re-measure of M16 after the pin: drop the named stamp step added to no-snapshot-available

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-d.json`, row `M16_named_stamp_step_dropped_remeasured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 684 against a baseline of 684
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-identity-2026-08-01T000000Z-the snapshot 2026-08-01T000000Z was not found]`

Old text:

```
            "when --snapshot named a stamp, that snapshot or its database "
            "folder is not on the remote; check the stamp, or leave the flag "
            "off to take the newest",

```

New text:

```
(empty)
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

### `r679-a.E1_cli_offers_every_verdict`

review resolve: offer the whole enum as --verdict choices

- File: `src/cratekit/cli/review.py`
- Source: `r679-a.json`, row `E1_cli_offers_every_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 833 against a baseline of 833
- Kills: 1 (killed)
- Killed:
  - `tests/test_review_queue.py::test_the_command_line_offers_a_person_only_the_persons_verdicts`

Old text:

```
        choices=tuple(str(member) for member in review.PERSON_VERDICTS),
```

New text:

```
        choices=tuple(str(member) for member in review.Verdict),
```

### `r679-a.E2_listing_drops_the_actor`

review list: leave the actor out of the listing, so a superseded row shows no rule

- File: `src/cratekit/cli/review.py`
- Source: `r679-a.json`, row `E2_listing_drops_the_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 833 against a baseline of 833
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

### `r185-r246-author.D2_cloud_gate_restored`

Declare the cloud sync decision on a verb that opens no database, the half the contract suite calls spurious

- File: `src/cratekit/cli/registry.py`
- Source: `r185-r246-author.json`, row `D2_cloud_gate_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the cloud sync gate is added to tag.retag's gates, the entry before name.apply, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5846 against a baseline of 5846
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
- Collected: 5846 against a baseline of 5846
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

### `r770-d.C8_native_gate_answered_inline`

registry: declare intake.file.native as an ordinary gate, answerable on the run that found it

- File: `src/cratekit/cli/registry.py`
- Source: `r770-d.json`, row `C8_native_gate_answered_inline`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; intake.file.native's explicit flag is the same value, flipped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_cli_contract.py`
- Collected: 1031 against a baseline of 1031
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

### `u103-b.M1_identify_declared_adjudicating`

Take the adjudicates declaration off intake.identify

- File: `src/cratekit/cli/registry.py`
- Source: `u103-b.json`, row `M1_identify_declared_adjudicating`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; intake.identify's adjudicates flag is the same value, dropped the same way
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_cli_contract.py`
- Collected: 1064 against a baseline of 1065
- Kills: 1 (collect-error)
- Note: collection changed: 1064 collected against a baseline of 1065. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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

### `u39-author-full.W2_unreachable_gate_restored`

name.apply redeclares the cloud sync decision its work can never raise

- File: `src/cratekit/cli/registry.py`
- Source: `u39-author-full.json`, row `W2_unreachable_gate_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the cloud sync gate is added to name.apply's gates, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 4044 against a baseline of 4044
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

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on setbuild, above its landed comment, as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4176 against a baseline of 4180
- Kills: 33 (collect-error)
- Note: collection changed: 4176 collected against a baseline of 4180. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_count_below_one_is_the_parsers_verdict_and_not_a_refusal`
  - `tests/test_setbuilder_cli.py::test_a_key_off_the_wheel_is_the_parsers_verdict`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[path]`
  - `tests/test_setbuilder_cli.py::test_a_name_beside_another_anchor_form_is_the_parsers_verdict[unowned]`
  - `tests/test_setbuilder_cli.py::test_a_name_the_library_does_not_hold_refuses_as_not_indexed`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_a_path_and_an_unowned_label_together_are_the_parsers_verdict`
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_a_supplied_key_beside_a_name_refuses_rather_than_being_ignored`
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
- Collected: 4252 against a baseline of 4253
- Kills: 2 (collect-error)
- Note: collection changed: 4252 collected against a baseline of 4253. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_verb_carrying_a_resume_argv_builder_declares_that_it_queues`
  - `tests/test_master_cli.py::test_the_entry_is_landed_and_declares_no_gate`

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
- Collected: 4372 against a baseline of 4376
- Kills: 58 (collect-error)
- Note: collection changed: 4372 collected against a baseline of 4376. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`
  - `tests/test_backup_cli.py::test_a_backup_to_a_destination_nobody_is_backing_up_to_is_its_own_job`
  - `tests/test_backup_cli.py::test_a_contained_analysis_share_draws_no_warning_from_the_verb`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`
  - `tests/test_backup_cli.py::test_a_job_that_can_never_run_does_not_stand_in_for_a_backup`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_library_with_an_identity_draws_no_such_warning`
  - ... and 43 more, see the JSON sidecar

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
- Collected: 4375 against a baseline of 4376
- Kills: 6 (collect-error)
- Note: collection changed: 4375 collected against a baseline of 4376. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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
- Collected: 1038 against a baseline of 1038
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

### `u161.G1_pin_never_compared`

Gates.require: skip the pin comparison, so an answer given over one file is used by a run that opened another

- File: `src/cratekit/cli/gates.py`
- Source: `u161.json`, row `G1_pin_never_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_pins.py`, `tests/test_intake_land_native.py`, `tests/test_gate_shown_plan.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

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
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

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
- Collected: 66 against a baseline of 66
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
- Collected: 66 against a baseline of 66
- Kills: 24 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_pins.py::test_the_same_pin_on_the_continuation_takes_the_recorded_answer`
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
  - ... and 9 more, see the JSON sidecar

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
- Collected: 66 against a baseline of 66
- Kills: 24 (killed)
- Killed:
  - `tests/test_gate_pins.py::test_a_pinned_run_asked_with_no_pin_is_stale_too`
  - `tests/test_gate_pins.py::test_another_pin_with_the_same_digest_is_stale_and_names_both_values`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_pins.py::test_the_same_pin_on_the_continuation_takes_the_recorded_answer`
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
  - ... and 9 more, see the JSON sidecar

Old text:

```
                for name, one in (data.get("pins") or {}).items()
```

New text:

```
                for name, one in {}.items()
```

### `u49-author.G2_the_second_raise_site_drops_the_context`

Carry the context at the no-answer refusal only, so what a person sees depends on whether they typed a flag

- File: `src/cratekit/cli/gates.py`
- Source: `u49-author.json`, row `G2_the_second_raise_site_drops_the_context`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 1992 against a baseline of 1992
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

### `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound`

The handler key goes back to declaring no worker, which is the state this whole unit exists to leave

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R39_tag_folder_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 359 against a baseline of 359
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
- Collected: 359 against a baseline of 359
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

### `u58-workers-and-wav.H1_run_unbound`

Drop the analyze.run binding from the handler table

- File: `src/cratekit/cli/handlers.py`
- Source: `u58-workers-and-wav.json`, row `H1_run_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 613 against a baseline of 613
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

### `r678-a.A2_drop_the_import_proof_case`

the original defect for intake imported: render never asks for the proof

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A2_drop_the_import_proof_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 89 against a baseline of 89
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

### `r925.R4_version_unsaid`

The human line drops a track's version

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R4_version_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
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

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7236 against a baseline of 7236
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
- Collected: 7236 against a baseline of 7236
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
- Collected: 7236 against a baseline of 7236
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
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
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

### `r924.D1_json_gets_progress`

The dispatcher hands the progress writer to JSON output too, so standard error carries progress under --output json

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D1_json_gets_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
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
- Collected: 52 against a baseline of 52
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

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1118 against a baseline of 1118
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

### `u248.L4_listing_drops_the_stub_line`

ask_for_listing: a missing extra no longer makes the stub, so the listing omits (requires the extra)

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L4_listing_drops_the_stub_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 1207 against a baseline of 1207
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

### `u212.S1_missing_ends`

sync_land._missing: nothing listed ends the pass whatever is staged

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S1_missing_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 318 against a baseline of 318
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

### `u212.S4_staged_said`

sync_land._missing: the missing row drops the staged clause, so the pass does not say how many it skipped

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S4_staged_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 318 against a baseline of 318
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

### `r925.J2_playlist_excluded`

job show lists tracks for a set job only, not a playlist job

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J2_playlist_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`
  - `tests/intake/test_workers.py::test_the_intake_keys_resolve_to_the_one_worker_and_the_job_verbs_spell_them_alike`

Old text:

```
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set", "intake.playlist"})
```

New text:

```
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set"})
```

### `r925.J3_field_not_set`

job show computes the tracks and never puts them on the envelope

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J3_field_not_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_job_of_another_handler_lists_no_tracks_and_is_not_driven_under_this_envelope`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`

Old text:

```
    if tracks is not None:
        summary[TRACKS_FIELD] = tracks
```

New text:

```
    if tracks is None:
        summary[TRACKS_FIELD] = tracks
```

### `r925.J4_isrc_dropped`

job show lists every track without its ISRC

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J4_isrc_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`

Old text:

```
                "isrc": str(said["isrc"]) if said.get("isrc") else None,
```

New text:

```
                "isrc": None,
```

### `r925.J5_version_dropped`

job show lists every track without its version

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J5_version_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`

Old text:

```
                "version": str(said.get("version") or ""),
```

New text:

```
                "version": "",
```

### `u182.M17_summary_playlist`

_summary: carry no playlist field, so job show and job list say nothing of it

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M17_summary_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 206 against a baseline of 206
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[hearts-job]`
  - `tests/test_jobs.py::test_a_stale_set_or_hearts_job_names_no_playlist_and_says_what_it_frees[set-job]`
  - `tests/test_jobs.py::test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for`

Old text:

```
    named = intake_playlist(job)
    if named is not None:
```

New text:

```
    named = None
    if named is not None:
```

### `u172-b.C3_left_miscounted`

guess: count the files left as the candidates written rather than the files still without a genre

- File: `src/cratekit/cli/tail.py`
- Source: `u172-b.json`, row `C3_left_miscounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_the_files_left_are_the_files_still_without_a_genre`

Old text:

```
    left = count - after - unread
```

New text:

```
    left = count - before - written - unread
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

### `u172.C2_guess_without_pass`

guess_argv: never name the pass, so no playlist votes in a pass

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C2_guess_without_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`
  - `tests/test_tag_guess.py::test_the_guess_is_named_with_a_pass_only_when_one_is_given`

Old text:

```
*([PASS_FLAG, pass_name] if pass_name else [])
```

New text:

```
*([])
```

### `u181.T1_rescore_ignores_unable`

tail.rescore: queue the rescore although the model cannot score here

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T1_rescore_ignores_unable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
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

### `u181.T2_rescore_ignores_profile`

tail.rescore: run the vocals verb on a profile with the vocals module off

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T2_rescore_ignores_profile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_vocals_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    if not vocals_on(cfg):
        chain.summary["vocal_rescore"] = "off"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "off"
```

### `u181.T3_rescore_keeps_stale`

tail.rescore: leave a stale vocals job over the folder open

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T3_rescore_keeps_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_replaces_a_stale_vocals_job_over_the_folder`

Old text:

```
        replace_stale(chain, ANALYZE, VOCALS_VERB, folder, cfg)
```

New text:

```
        pass
```

### `u181.T4_rescore_failure_ignored`

tail.rescore: a vocals job that did not succeed is reported scored and the chain goes on

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T4_rescore_failure_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_rescore_job_that_does_not_succeed_ends_the_chain_at_the_analyze_step`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
        raise Stop(ANALYZE, job_error(chain, job))
    chain.summary["vocal_rescore"] = count
```

New text:

```
    chain.summary["vocal_rescore"] = count
```

### `u212.T1_reason_guard`

tail.second_copies: read any refusal's outstanding files, not only rename-incomplete's

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T1_reason_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1608 against a baseline of 1608
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_stop_that_is_not_rename_incomplete_or_cannot_read_the_queue_is_unchanged`

Old text:

```
    if cause.reason != RENAME_INCOMPLETE:
        return stop
```

New text:

```
(empty)
```

### `u212.T2_done_only`

tail._downloaded_by: a job that froze the track and never acquired it is named as its source

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T2_done_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1608 against a baseline of 1608
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if refs & done:
```

New text:

```
            if refs:
```

### `u212.T3_library`

tail._downloaded_by: another library's download job is named

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T3_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1608 against a baseline of 1608
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if cfg is not None and job.library_id != cfg.library.volume_id:
                continue
```

New text:

```
(empty)
```

### `u212.T4_earliest_first`

tail._downloaded_by: the passes named newest first, though the step says earliest first

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T4_earliest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1608 against a baseline of 1608
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
        for job in reversed(jobs.list_jobs(store)):
```

New text:

```
        for job in jobs.list_jobs(store):
```

### `u212.T5_name_wraps`

tail.name: the name step's stop passed on without the passes that downloaded the copy

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T5_name_wraps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1608 against a baseline of 1608
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_name_stop_over_a_second_copy_names_the_pass_that_downloaded_it`
  - `tests/test_sync_land_staged.py::test_a_second_copy_no_download_job_records_is_said_so`

Old text:

```
        raise second_copies(stop, cfg) from None
```

New text:

```
        raise stop from None
```

### `u284.T1_pass_names_nothing`

tail.tail_step: the pass never names the files the catalogues refused

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T1_pass_names_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_a_token_the_pass_reaches_its_landing_and_names_the_refused_files`

Old text:

```
    if step == TAG:
        refused_files(chain, chain.settled.get(step))
```

New text:

```
    if False:
        refused_files(chain, chain.settled.get(step))
```

### `u284.T2_pass_stop_unsaid`

tail.tail_step: the pass's stop at its tag step says nothing of who refused or the token

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T2_pass_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        raise Stop(step, refused_stop(error, chain.settled.get(step)) if step == TAG else error)
```

New text:

```
        raise Stop(step, error)
```

### `u319.M10_sync_stop_drops_the_short_path`

tail: the step crate sync land prints names one path again

- File: `src/cratekit/cli/tail.py`
- Source: `u319.json`, row `M10_sync_stop_drops_the_short_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}; "
    f"{AUTO_ANALYSIS_STEP}",
```

New text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}",
```

