# r390-a.A1, driven by hand at both commits

`r390-a.A1_retry_re_arms_unconditionally` deletes the refusal in
`src/cratekit/core/jobs.py` that stops a job whose cause is not retryable from
being resumed. Batch 06 of the before side read it as an error, and batch
`u331-before-d-01`, measured again on a fresh container at `5b957acb`, read it
as an error again (`OSError: [Errno 39] Directory not empty: 'popen-gw0'`,
pytest's own cleanup under the xdist temporary root), the shape U325 met and
drove by hand in `docs/mutation/u325-replay/r390-driven.md`. On the after side
the driver measured it (`u331-after-d-01` at `d29860c2`: killed, 5).

So it is driven by hand here at both commits, the way U325 did. Driven on
2026-11-24 on one container, in a worktree with its own `.venv`, one process
(`-n 0`), `PYTHONDONTWRITEBYTECODE=1`, the row's own three files
(`tests/test_jobs.py`, `tests/test_master_cli.py`,
`tests/test_acquire_workers.py`), the row's substitution applied as text, the
file restored from `git show HEAD` and read equal to it afterwards. Each run
unmutated fails one test, the same one, which is the machine's; the deaths
below are the tests that fail mutated and pass unmutated.

On `5b957acb` (before, `main`'s source at `b8d6d1d8`) and on `637467cb`
(after, the branch), the same five tests fail:

- `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
- `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
- `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
- `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
- `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

They are the five U325 found. So the row is killed before and after by the
same tests, and U331 lost nothing here. It stays an error in the before
tables, as the driver read it.
