# Mutation table: r290-author

Measured by `scripts/mutate.py` on 2026-09-20 19:09 UTC, branch `relay/160` at `e0e0176`. Pass kind: light.

Baseline: green, 9247 collected. pytest invocations for this batch: 32.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 9247 against 9247. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 45 | killed |
| `J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 44 | killed |
| `J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 88 | killed |
| `J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 24 | killed |
| `J5_causeless_block_returns` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 1 | killed |
| `J6_causeless_block_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 1 | killed |
| `J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 1928 | 19 | killed |
| `D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 5704 | 43 | killed |
| `D2_parked_marked_resumable` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 5704 | 2 | killed |
| `D3_resumable_read_off_the_code_alone` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 5704 | 1 | killed |
| `D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 5704 | 18 | killed |
| `R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 177 | 2 | killed |
| `R2_backup_rebuild_drops_the_type` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 201 | 2 | killed |
| `R3_the_owner_drops_the_type` | `src/cratekit/core/cause.py` | user | 3 file(s) | 262 | 4 | killed |
| `S01_master_call_removed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 158 | 9 | killed |
| `S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 164 | 9 | killed |
| `S03_acquire_fallback_call_removed` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 151 | 6 | killed |
| `S04_backup_call_removed` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 201 | 11 | killed |
| `S05_intake_call_removed` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 116 | 11 | killed |
| `S06_label_call_removed` | `src/cratekit/label/cli.py` | user | 2 file(s) | 195 | 15 | killed |
| `S07_rebuild_call_removed` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 116 | 6 | killed |
| `S08_route_resort_call_removed` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 251 | 7 | killed |
| `S11_tagging_shell_call_removed` | `src/cratekit/tagging/shell.py` | user | 2 file(s) | 177 | 18 | killed |
| `S12_adopt_shell_call_removed` | `src/cratekit/adopt/shell.py` | user | 2 file(s) | 146 | 11 | killed |
| `S13_outbound_shell_call_removed` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 183 | 17 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `S09_analysis_call_removed`: Remove the one jobs.raise_for_state call from analysis/cli.py Dropped because: ranked below the cap: the same one line in the same shape as S05, S07 and S11, killed by the same parametrized population test, and the static guard reads this shell as well
- `S10_vocals_call_removed`: Remove the one jobs.raise_for_state call from vocals/cli.py Dropped because: ranked below the cap: the same one line in the same shape as S05, S07 and S11, killed by the same parametrized population test, and the static guard reads this shell as well

## Row definitions

### `J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
- Kills: 45 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - ... and 30 more, see the JSON sidecar

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

### `J2_blocked_raises_the_plain_type`

Raise a plain CratekitError for a parked job, so the verb exits non zero and the outcome word says failed

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
- Kills: 44 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - ... and 29 more, see the JSON sidecar

Old text:

```
        raise JobBlocked(job.cause)
```

New text:

```
        raise CratekitError(job.cause)
```

### `J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
- Kills: 88 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_refusal_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - ... and 73 more, see the JSON sidecar

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

### `J4_predicate_narrowed_to_failed`

Narrow the closed predicate to FAILED alone, so a run stopped by a signal is reported through a normal envelope

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
- Kills: 24 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - ... and 9 more, see the JSON sidecar

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

### `J5_causeless_block_returns`

Return for a blocked job that records no reason, reading a missing reason as a missing problem

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
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

### `J6_causeless_block_raises_the_plain_type`

Refuse a blocked job that records no reason as a plain error, so the envelope says failed over a row the job listing calls blocked

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
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

### `J7_cancelled_raises_the_plain_type`

Raise a plain CratekitError for a cancelled job, so a person who stopped a run is told it failed

- File: `src/cratekit/core/jobs.py`
- Surface: user
- Subset: test files importing cratekit.core.jobs
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 1928 against a baseline of 1928
- Kills: 19 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.favorites]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
            raise JobCancelled(job.cause)
```

New text:

```
            raise CratekitError(job.cause)
```

### `D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Surface: user
- Subset: test files importing cratekit.cli
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5704 against a baseline of 5704
- Kills: 43 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
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
  - ... and 28 more, see the JSON sidecar

Old text:

```
        parked = isinstance(exc, JobBlocked)
```

New text:

```
        parked = False
```

### `D2_parked_marked_resumable`

Mark a parked job's envelope resumable, which sends a wrapper to crate run for work only the verb can continue

- File: `src/cratekit/cli/__init__.py`
- Surface: user
- Subset: test files importing cratekit.cli
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5704 against a baseline of 5704
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

### `D3_resumable_read_off_the_code_alone`

Derive resumable from the cause's code alone again, so a worker parking on a gate coded cause tells a wrapper the gate run can continue the job

- File: `src/cratekit/cli/__init__.py`
- Surface: user
- Subset: test files importing cratekit.cli
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5704 against a baseline of 5704
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`

Old text:

```
        resumable = cause.code in gates.GATE_CODES and not parked
```

New text:

```
        resumable = cause.code in gates.GATE_CODES
```

### `D4_cancelled_reads_failed`

Read the cancelled type as the failed outcome, which is what the dispatcher said before Outcome.CANCELLED had a producer

- File: `src/cratekit/cli/__init__.py`
- Surface: user
- Subset: test files importing cratekit.cli
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 5704 against a baseline of 5704
- Kills: 18 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[rebuild]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.favorites]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
            outcome = Outcome.CANCELLED
```

New text:

```
            outcome = Outcome.FAILED
```

### `R1_retag_rebuild_drops_the_type`

Rebuild the retag refusal as a plain CratekitError again, so a retag parked after correcting a file says failed

- File: `src/cratekit/tagging/retag_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `R2_backup_rebuild_drops_the_type`

Rebuild the backup rehearsal refusal as a plain CratekitError again, so a rehearsal the worker parked says failed

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `R3_the_owner_drops_the_type`

Make cause.rebuilt return the plain type for every input, so both hops drop the blocked bit at once with no hand written rebuild for the static guard to find

- File: `src/cratekit/core/cause.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_backup_cli.py`
- Collected: 262 against a baseline of 262
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause[JobBlocked]`
  - `tests/test_job_outcome.py::test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause[JobCancelled]`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`

Old text:

```
            return kind(cause)
```

New text:

```
            return CratekitError(cause)
```

### `S01_master_call_removed`

Remove the one jobs.raise_for_state call from master/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/master/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_master_cli.py`
- Collected: 158 against a baseline of 158
- Kills: 9 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_job_outcome.py::test_the_dispatcher_reads_the_blocked_type_as_the_blocked_outcome`
  - `tests/test_master_cli.py::test_a_failed_job_stays_resumable_and_the_second_attempt_redoes_that_item`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S02_acquire_download_call_removed`

Remove the one jobs.raise_for_state call from acquire/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/acquire/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_acquire_workers.py`
- Collected: 164 against a baseline of 164
- Kills: 9 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_refusal_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S03_acquire_fallback_call_removed`

Remove the one jobs.raise_for_state call from acquire/fallback_cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/acquire/fallback_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 151 against a baseline of 151
- Kills: 6 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S04_backup_call_removed`

Remove the one jobs.raise_for_state call from backup/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/backup/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 201 against a baseline of 201
- Kills: 11 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_half_failed_rehearsal_says_it_too_on_the_other_refusal`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S05_intake_call_removed`

Remove the one jobs.raise_for_state call from intake/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/intake/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 116 against a baseline of 116
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.set]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S06_label_call_removed`

Remove the one jobs.raise_for_state call from label/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/label/cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_label_workers.py`
- Collected: 195 against a baseline of 195
- Kills: 15 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[sync.labels]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[sync.labels]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[label.import]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[sync.labels]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_label_workers.py::test_a_label_the_registry_no_longer_holds_refuses_rather_than_sweeping_nothing`
  - `tests/test_label_workers.py::test_a_resume_of_a_cancelled_sweep_does_not_exit_ok_over_the_items_it_never_ran`
  - `tests/test_label_workers.py::test_a_second_resume_of_a_failed_sweep_still_does_not_exit_ok`
  - `tests/test_label_workers.py::test_a_sweep_whose_failures_are_permanent_does_not_tell_the_person_to_resume`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S07_rebuild_call_removed`

Remove the one jobs.raise_for_state call from cli/rebuild.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/cli/rebuild.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 116 against a baseline of 116
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

### `S08_route_resort_call_removed`

Remove the one jobs.raise_for_state call from write/routing_cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/write/routing_cli.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_routing_workers.py`
- Collected: 251 against a baseline of 251
- Kills: 7 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[resort]`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/tagging/shell.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 18 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.folder]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[tag.retag]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_tag_workers.py::test_a_cancelled_job_raises_rather_than_reporting_through_a_normal_envelope`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - ... and 3 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S12_adopt_shell_call_removed`

Remove the one jobs.raise_for_state call from adopt/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/adopt/shell.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_adopt_workers.py`
- Collected: 146 against a baseline of 146
- Kills: 11 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item`
  - `tests/test_adopt_workers.py::test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.apply]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `S13_outbound_shell_call_removed`

Remove the one jobs.raise_for_state call from modules/outbound/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/modules/outbound/shell.py`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_outbound_workers.py`
- Collected: 183 against a baseline of 183
- Kills: 17 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[sync.favorites]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[sync.favorites]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_an_item_whose_track_left_the_export_refuses_rather_than_writing_nothing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

