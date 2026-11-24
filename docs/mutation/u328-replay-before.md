# Mutation table: u328-replay-before

Measured by `scripts/mutate.py` on 2026-11-23 20:45 UTC, branch `cloud/977-no-source-file-over-1500-lines` at `c22d75ce`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22797 collected. pytest invocations for this batch: 62.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `8834a07f6cd0`, and this tree is at `c22d75cef752`).

Subset baselines: 25, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `docs/mutation/u328-replay-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22797 against 22797. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
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

## Row definitions

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

