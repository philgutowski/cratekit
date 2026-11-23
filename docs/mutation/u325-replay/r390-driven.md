# r390-a.A1, driven by hand at both commits

`r390-a.A1_retry_re_arms_unconditionally` deletes the refusal in
`src/cratekit/core/jobs.py` that stops a job whose cause is not retryable from
being resumed. #855's batch b read it as an error, from pytest's own cleanup
(`Directory not empty: 'popen-gw0'`), the shape U298's H9 met, so it is driven
by hand here as `docs/mutation/u298-h9-driven.md` drove H9.

The same text stands once at both commits, in place. Driven on 2026-11-23 on
this container, one xdist worker, `PYTHONDONTWRITEBYTECODE=1`, the row's own
three files (`tests/test_jobs.py`, `tests/test_master_cli.py`,
`tests/test_acquire_workers.py`), failures read net of the scratch copy of the
machine's failures each worktree read. The source was restored and read equal
to `git show HEAD` afterwards, and the files run again unmutated fail nothing
net of the machine's.

On `539638eb` (before) and on `db120fdb` (after), the same five tests fail:

- `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
- `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
- `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
- `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
- `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

So the row is killed before and after by hand, by the same tests, and U298
lost nothing here. It stays an error in the before table, as the driver read
it, and is left out of the after batches.
