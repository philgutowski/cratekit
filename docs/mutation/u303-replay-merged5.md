# Mutation table: u303-replay-merged5

Measured by `scripts/mutate.py` on 2026-11-23 06:42 UTC, branch `cloud/860-cli-fifth-smaller` at `041c5150`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22531 collected. pytest invocations for this batch: 34.

Full baseline: measured by this driver (the battery's verdict was not read: it was read against another known failures file).

Subset baselines: 7, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `docs/mutation/u303-replay-known-failures.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22531 against 22531. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r787.D1_doctor_own_list` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 4 | killed |
| `r787.D2_set_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 1 | killed |
| `r787.D3_source_guard_removed` | `src/cratekit/cli/doctor_state.py` | user | 12 file(s) | 2220 | 1 | killed |
| `u132.D1_doctor_behind` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 2 | killed |
| `u132.D2_doctor_defect` | `src/cratekit/cli/doctor_library.py` | user | 12 file(s) | 2220 | 1 | killed |
| `u206.M24_doctor_set_aside_unnamed` | `src/cratekit/cli/doctor_state.py` | user | 9 file(s) | 1130 | 1 | killed |
| `r185-r246-author.D2_cloud_gate_restored` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5846 | 2 | killed |
| `r312.R1_summary_promises_a_replace` | `src/cratekit/cli/registry.py` | user | 44 file(s) | 5846 | 1 | killed |
| `u112.G1_part_unverified` | `src/cratekit/cli/gates.py` | user | 2 file(s) | 212 | 1 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7247 | 47 | killed |
| `r290-author.D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7247 | 2 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7247 | 22 | killed |
| `u206.M23_lookup_line_dropped` | `src/cratekit/cli/__init__.py` | user | 9 file(s) | 1130 | 3 | killed |
| `u210.R24_continue_run` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 132 | 1 | killed |
| `u152.R14_download_list_match` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R15_download_newest` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R16_download_cancelled` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R17_download_retry` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R20_nothing_downloaded` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 2 | killed |
| `u152.R2_preflight_backup` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R6_lift_failed_checks` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 2 | killed |
| `u152.R7_outbound_held` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 2 | killed |
| `u152.R8_continue_open_pass` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R9_open_passes_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R13_missing_lift` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |

## Row definitions

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

### `u206.M24_doctor_set_aside_unnamed`

_check_isrc_cache: leave the set aside files out of the note

- File: `src/cratekit/cli/doctor_state.py`
- Source: `u206.json`, row `M24_doctor_set_aside_unnamed`
- Moved: the same text, now in src/cratekit/cli/doctor_state.py, was in src/cratekit/cli/doctor.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
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

### `u112.G1_part_unverified`

hand_off carries any digest a caller names as the part, whatever the answer was given over

- File: `src/cratekit/cli/gates.py`
- Source: `u112.json`, row `G1_part_unverified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_sync_all.py`
- Collected: 212 against a baseline of 212
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

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7247 against a baseline of 7247
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
- Collected: 7247 against a baseline of 7247
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
- Collected: 7247 against a baseline of 7247
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

### `u206.M23_lookup_line_dropped`

_with_isrc_lookups: never add the isrc-lookups line

- File: `src/cratekit/cli/__init__.py`
- Source: `u206.json`, row `M23_lookup_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
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

### `u152.R14_download_list_match`

_download_job: drop the list match, so another list's download job is read as the pass's

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R14_download_list_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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

### `u152.R13_missing_lift`

_missing: carry none of the listing's failing rows

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R13_missing_lift`
- Moved: U303 shortened the comment above the call to one line; the lift of the listing's failing rows in _missing, the guard this row removes, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1184 against a baseline of 1184
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`

Old text:

```
    # The listing's failing rows ride through, so an unnameable track is said.
    _lift_failed_checks(report, envelope)

```

New text:

```
    # The listing's failing rows ride through, so an unnameable track is said.

```

