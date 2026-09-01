# Mutation table: u46-round-2

Measured by `scripts/mutate.py` on 2026-09-01 21:41 UTC, branch `relay/64` at `9aaeef7`. Pass kind: light.

Baseline: green, 6476 collected. pytest invocations for this batch: 6.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 6476 against 6476. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `M2_resume_does_not_drive` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 10 | killed |
| `M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 2 | killed |
| `M7B_engine_refusal_swallowed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 40 | 13 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `M10_report_path_recomputed`: Derive the staged path with output_path instead of reading it off the engine's report Dropped because: expected inert and dropped rather than run: the two agree by construction, so no test can tell them apart. The reason to read the report is the one this module's docstring already gives, that two name builders for one file is how an in-place write arrives later. Recorded so the absence is visible rather than read as coverage

## Row definitions

### `M2_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 10 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_failed_job_stays_resumable_and_the_second_attempt_redoes_that_item`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
```

New text:

```
                pass
```

### `M6_staging_not_cleared`

Leave a previous attempt's partial encode in the staging directory

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `M7B_engine_refusal_swallowed`

Translate the engine's encoder-failed into a generic internal defect

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: test files importing cratekit.master.cli
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 40 against a baseline of 40
- Kills: 13 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - `tests/test_master_cli.py::test_an_existing_master_refuses_without_overwrite_and_proceeds_with_it`
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
            str(exc.refusal),
            exc.detail,
```

New text:

```
            "internal-error",
            "the mastering engine refused",
```

