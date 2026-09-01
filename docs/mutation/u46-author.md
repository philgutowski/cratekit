# Mutation table: u46-author

Measured by `scripts/mutate.py` on 2026-09-01 21:12 UTC, branch `relay/64` at `b0cee3c`. Pass kind: light.

Baseline: green, 6476 collected. pytest invocations for this batch: 25.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6476 against 6476. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `H1_binding_removed` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 15 | killed |
| `H2_is_known_always_true` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 3 | killed |
| `H3_import_before_refusing` | `src/cratekit/cli/handlers.py` | maintainer | 3 file(s) | 60 | 1 | killed |
| `H4_unbound_reason_silent` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 2 | killed |
| `H5_fresh_config` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 1 | killed |
| `H6_no_drive_call` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 16 | killed |
| `H7_no_drift` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 1 | killed |
| `H8_drift_wording_dropped` | `src/cratekit/cli/handlers.py` | user | 3 file(s) | 60 | 1 | killed |
| `M1_no_items_enqueued` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 11 | killed |
| `M2_resume_does_not_drive` | `src/cratekit/master/cli.py` | user | 2 file(s) | 0 | collection error | collect-error |
| `M3_payload_source_not_item` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 2 | killed |
| `M4_no_destination_check` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 1 | killed |
| `M5_encode_at_destination` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 3 | killed |
| `M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 2 file(s) | 6476 | 0 (promoted) | zero |
| `M7_report_not_read` | `src/cratekit/master/cli.py` | user | 2 file(s) | 6476 | 0 (promoted) | zero |
| `M8_relative_path_frozen` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 1 | killed |
| `J1_worker_state_unreported` | `src/cratekit/cli/jobs.py` | user | 4 file(s) | 6476 | 1 (promoted) | killed |

## Zero rows and what they owe

- `M6_staging_not_cleared` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `M7_report_not_read` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `H9_declaration_separator`: Accept a declaration with no colon rather than refusing it Dropped because: ranked below the cap: the same refusal family as H3, which is measured, and its only reachable input is a table this repository writes by hand
- `M9_staging_dirname`: Rename the staging directory constant Dropped because: ranked below the cap: a name with no behaviour attached; M5 and M6 measure what staging actually buys
- `C1_context_run_job_removed`: Delete Context.run_job so no verb can reach the driver Dropped because: ranked below the cap: strictly weaker than M2, which removes the only call to it and is measured

## Row definitions

### `H1_binding_removed`

Unbind master, so no verb in the build has a handler at all

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
- Kills: 15 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_handlers.py::test_is_known_answers_for_a_declared_key_and_an_invented_one`
  - `tests/test_handlers.py::test_the_declared_population_is_not_empty`
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_a_failed_job_stays_resumable_and_the_second_attempt_redoes_that_item`
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_naming_a_job_reports_it_rather_than_queueing_a_second`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
    "master": "cratekit.master.cli:handle",
```

New text:

```
(empty)
```

### `H2_is_known_always_true`

Claim every handler key is bound, including the eighteen that are not

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
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

### `H3_import_before_refusing`

Import the declared module before checking the key is real, defeating KTD26

- File: `src/cratekit/cli/handlers.py`
- Surface: maintainer
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
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

### `H4_unbound_reason_silent`

Stop saying why a queued verb has no worker

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_unbound_verb_says_why_and_every_bound_one_says_nothing`
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`

Old text:

```
    return HANDLERS_NOT_YET_BOUND.get(key)
```

New text:

```
    return None
```

### `H5_fresh_config`

Hand the handler a freshly loaded configuration instead of the frozen one

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_the_handler_receives_the_frozen_configuration_and_not_the_current_one`

Old text:

```
    frozen = jobs.frozen_config(job)
```

New text:

```
    frozen = config.load()
```

### `H6_no_drive_call`

Return an empty result rather than driving the job

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
- Kills: 16 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between`
  - `tests/test_handlers.py::test_a_handler_that_produces_a_file_has_it_committed_and_recorded`
  - `tests/test_handlers.py::test_exactly_one_place_in_the_package_calls_the_job_driver`
  - `tests/test_handlers.py::test_the_handler_receives_the_frozen_configuration_and_not_the_current_one`
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_a_failed_job_stays_resumable_and_the_second_attempt_redoes_that_item`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_report_naming_a_file_that_is_not_there_fails_the_item`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    return jobs.drive(store, job.job_id, handle, root=root, current_config=current)
```

New text:

```
    return jobs.DriveResult(job=job)
```

### `H7_no_drift`

Never compute drift, so a moved configuration is silently chosen between

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_a_configuration_that_moved_is_reported_as_drift_rather_than_chosen_between`

Old text:

```
        current: config.Config | None = config.load()
```

New text:

```
        current: config.Config | None = None
```

### `H8_drift_wording_dropped`

Report drift without naming what moved

- File: `src/cratekit/cli/handlers.py`
- Surface: user
- Subset: test files importing cratekit.cli.handlers
- Ran: `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 60 against a baseline of 60
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

### `M1_no_items_enqueued`

Queue the recording with no item, so the driver has nothing to claim

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 11 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_failed_job_stays_resumable_and_the_second_attempt_redoes_that_item`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_report_naming_a_file_that_is_not_there_fails_the_item`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_queueing_a_recording_gives_the_driver_one_item_to_claim`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
            item_ids=(str(payload[SOURCE]),),
```

New text:

```
(empty)
```

### `M2_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 0 against a baseline of 40
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 40. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/test_job_seam.py`, `tests/test_master_cli.py`

Old text:

```
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
```

New text:

```
(empty)
```

### `M3_payload_source_not_item`

Read the recording from the payload rather than from the item the driver claimed

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`

Old text:

```
    source = Path(str(item.item_id or payload.get(SOURCE) or ""))
```

New text:

```
    source = Path(str(payload.get(SOURCE) or item.item_id or ""))
```

### `M4_no_destination_check`

Drop the handler's output-exists check, letting a commit replace a master somebody kept

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`

Old text:

```
    if source.is_file() and final.exists() and not payload.get(OVERWRITE):
```

New text:

```
    if False:
```

### `M5_encode_at_destination`

Point the engine straight at the destination, so a killed encode poisons the resume

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
        {SOURCE: str(source), OUTPUT_DIR: str(staged_into), OVERWRITE: True},
```

New text:

```
        {SOURCE: str(source), OUTPUT_DIR: output_dir, OVERWRITE: True},
```

### `M6_staging_not_cleared`

Leave a previous attempt's leftovers in the staging directory

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 6476 against a baseline of 6476
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `M7_report_not_read`

Commit the engine's reported output without checking the file is there

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 6476 against a baseline of 6476
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not staged.is_file():
```

New text:

```
    if False:
```

### `M8_relative_path_frozen`

Freeze the recording as typed, so a child in another directory masters another file

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_relative_recording_is_frozen_absolute_so_the_child_masters_the_same_file`

Old text:

```
        SOURCE: str(Path(recording).absolute()) if recording else recording,
```

New text:

```
        SOURCE: recording,
```

### `J1_worker_state_unreported`

Report every job as having a worker, including the eighteen that do not

- File: `src/cratekit/cli/jobs.py`
- Surface: user
- Subset: test files importing cratekit.cli.jobs
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_queued_resume_contract.py`
- Collected: 6476 against a baseline of 6476
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_master_cli.py::test_a_job_show_says_when_a_queued_verb_has_no_worker`

Old text:

```
        "worker": "bound" if handlers.is_known(job.handler_key) else "none",
```

New text:

```
        "worker": "bound",
```

