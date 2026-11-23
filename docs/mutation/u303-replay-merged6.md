# Mutation table: u303-replay-merged6

Measured by `scripts/mutate.py` on 2026-11-23 07:33 UTC, branch `cloud/860-cli-fifth-smaller` at `d6dc4d82`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22474 collected. pytest invocations for this batch: 68.

Full baseline: measured by this driver (the battery's verdict was not read: it was read against another known failures file).

Subset baselines: 21, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `docs/mutation/u303-replay-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22474 against 22474. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r757-c2.D1_due_a_day_late` | `src/cratekit/cli/doctor_backup.py` | maintainer | 4 file(s) | 727 | 1 | killed |
| `r787.D1_doctor_own_list` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 4 | killed |
| `r787.D2_set_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 1 | killed |
| `r787.D3_source_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 1 | killed |
| `r388-b.M12_listing_steps_say_take_a_backup` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 659 | 2 | killed |
| `r388-c.M13_credential_step_dropped` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 659 | 2 | killed |
| `r388-d.M16_named_stamp_step_dropped_remeasured` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 659 | 2 | killed |
| `u27-reports-round-1.S1_limit_floor` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.S2_truncation_row` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S3_summary_total` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-2.S5_handler_key_wrong` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-3-fixes.F1_as_of_falsiness` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-3-fixes.F5_gap_row_flood` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `r185-r246-author.D2_cloud_gate_restored` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5789 | 2 | killed |
| `r312.R1_summary_promises_a_replace` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5789 | 1 | killed |
| `u27-reports-round-1.R1_delete_review_precondition` | `src/cratekit/cli/registry.py` | user | 14 file(s) | 3856 | 2 | killed |
| `u39-author-full.W2_unreachable_gate_restored` | `src/cratekit/cli/registry.py` | user | 19 file(s) | 4019 | 1 | killed |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry.py` | maintainer | 21 file(s) | 4145 | collection error | collect-error |
| `u44-author.D1_registry_drops_long_running` | `src/cratekit/cli/registry.py` | maintainer | 22 file(s) | 4205 | collection error | collect-error |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4315 | collection error | collect-error |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4318 | collection error | collect-error |
| `u96-b.B1_no_library_check_declared` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1092 | 1 | killed |
| `u49-author.G1_an_explicit_gate_takes_an_inline_answer_again` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.G2_the_second_raise_site_drops_the_context` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1988 | 1 | killed |
| `u46-author.H1_binding_removed` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 19 | killed |
| `u46-author.H2_is_known_always_true` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 3 | killed |
| `u46-author.H3_import_before_refusing` | `src/cratekit/cli/handlers.py` | maintainer | 3 file(s) | 91 | 1 | killed |
| `u46-author.H4_unbound_reason_silent` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 1 | killed |
| `u46-author.H5_fresh_config` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 2 | killed |
| `u46-author.H7_no_drift` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 2 | killed |
| `u46-author.H8_drift_wording_dropped` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 91 | 1 | killed |
| `u52-item-derivation.B1_label_import_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 296 | 6 | killed |
| `u52-item-derivation.B2_sync_labels_unbound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 296 | 48 | killed |
| `u52-item-derivation.B3_sync_labels_wrong_worker` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 296 | 42 | killed |
| `u55-collection-reader.R30_scan_handler_bound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 241 | 6 | killed |
| `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 343 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 343 | 21 | killed |
| `u58-workers-and-wav.H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 8 file(s) | 597 | 33 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7191 | 47 | killed |
| `r290-author.D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7191 | 2 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7191 | 22 | killed |
| `u211.D4_only_the_scans_own_refusal_is_kept` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 137 | 1 | killed |
| `r349-a.A3_job_show_field` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 89 | 4 | killed |

## Row definitions

### `r757-c2.D1_due_a_day_late`

_check_full_comparison: say to run one only past the bound and not at it

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `r757-c2.json`, row `D1_due_a_day_late`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
    due = f". {run_one}" if days >= FULL_COMPARISON_DUE_DAYS else ""
```

New text:

```
    due = f". {run_one}" if days > FULL_COMPARISON_DUE_DAYS else ""
```

### `r787.D1_doctor_own_list`

doctor's _declared_trees keeps a list of its own, the routing tree alone, instead of asking cutover_trees

- File: `src/cratekit/cli/doctor_state.py`
- Source: `r787.json`, row `D1_doctor_own_list`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_cutover_cli.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_routing_workers.py`
- Collected: 2220 against a baseline of 2220
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
- Collected: 2220 against a baseline of 2220
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
- Collected: 2220 against a baseline of 2220
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
- Collected: 2220 against a baseline of 2220
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
- Collected: 2220 against a baseline of 2220
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

### `r388-b.M12_listing_steps_say_take_a_backup`

Replace the listing failure's first reserved step with the take a backup step it replaced

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-b.json`, row `M12_listing_steps_say_take_a_backup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 659 against a baseline of 659
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
- Collected: 659 against a baseline of 659
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
- Collected: 659 against a baseline of 659
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

### `r185-r246-author.D2_cloud_gate_restored`

Declare the cloud sync decision on a verb that opens no database, the half the contract suite calls spurious

- File: `src/cratekit/cli/registry.py`
- Source: `r185-r246-author.json`, row `D2_cloud_gate_restored`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; the cloud sync gate is added to tag.retag's gates, the entry before name.apply, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5789 against a baseline of 5789
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
- Collected: 5789 against a baseline of 5789
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

### `u27-reports-round-1.R1_delete_review_precondition`

Stop delete.review declaring the Trash check as a precondition

- File: `src/cratekit/cli/registry.py`
- Source: `u27-reports-round-1.json`, row `R1_delete_review_precondition`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; delete.review's checks are the same tuple, library.trash dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 3856 against a baseline of 3856
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
- Collected: 4019 against a baseline of 4019
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
- Collected: 4145 against a baseline of 4149
- Kills: 33 (collect-error)
- Note: collection changed: 4145 collected against a baseline of 4149. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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
- Collected: 4205 against a baseline of 4206
- Kills: 2 (collect-error)
- Note: collection changed: 4205 collected against a baseline of 4206. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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
- Collected: 4315 against a baseline of 4319
- Kills: 49 (collect-error)
- Note: collection changed: 4315 collected against a baseline of 4319. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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
- Collected: 4318 against a baseline of 4319
- Kills: 6 (collect-error)
- Note: collection changed: 4318 collected against a baseline of 4319. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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

### `u96-b.B1_no_library_check_declared`

registry: declare library.mounted on the recovery verb, a check it needs to FAIL

- File: `src/cratekit/cli/registry.py`
- Source: `u96-b.json`, row `B1_no_library_check_declared`
- Moved: U303 laid the registry out a keyword run per line and shortened its comments; restore.bare-metal's checks are the same tuple, library.mounted added the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_cli_contract.py`
- Collected: 1092 against a baseline of 1092
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
- Collected: 1988 against a baseline of 1988
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

### `u46-author.H3_import_before_refusing`

Import the declared module before checking the key is real, defeating KTD26

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H3_import_before_refusing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
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

### `u46-author.H5_fresh_config`

Hand the handler a freshly loaded configuration instead of the frozen one

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H5_fresh_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
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

### `u46-author.H8_drift_wording_dropped`

Report drift without naming what moved

- File: `src/cratekit/cli/handlers.py`
- Source: `u46-author.json`, row `H8_drift_wording_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 91 against a baseline of 91
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
- Collected: 241 against a baseline of 241
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_both_adopt_keys_resolve_to_a_worker`
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
- Collected: 343 against a baseline of 343
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
- Collected: 343 against a baseline of 343
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
- Collected: 597 against a baseline of 597
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

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7191 against a baseline of 7191
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
- Collected: 7191 against a baseline of 7191
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
- Collected: 7191 against a baseline of 7191
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

### `r349-a.A3_job_show_field`

job show stops attaching the outcomes field

- File: `src/cratekit/cli/jobs.py`
- Source: `r349-a.json`, row `A3_job_show_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`

Old text:

```
        summary[backup_facts.OUTCOMES_FIELD] = outcomes
```

New text:

```
        pass
```

