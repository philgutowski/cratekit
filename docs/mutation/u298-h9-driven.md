# u298 H9, driven by hand

`H9_lock_now_held_elsewhere` reverts `config.lock_now`'s refusal: a lock another
process holds reads as had. The driver read the row as an error three times,
twice in `u298` (subset with `tests/test_config.py`) and once in `u298-h9`
(subset `tests/test_shared_homes.py` and `tests/test_jobs.py`), each time from
pytest's own temporary directory cleanup (`Directory not empty`): with the
mutation, a second job driver goes past the lock a live driver holds, and the
directory it then writes in is still busy when the session cleans up, so the
session ends without the summary line the driver reads.

Driven by hand on `cc6abb42` with the same mutation and the same two files
(`pytest tests/test_shared_homes.py tests/test_jobs.py`), the source restored
afterwards and checked clean, nine tests fail:

- `tests/test_shared_homes.py::test_a_lock_had_in_time_is_yielded_as_had_and_its_file_is_private_and_stays`
- `tests/test_shared_homes.py::test_a_lock_taken_without_waiting_is_had_by_one_and_read_by_the_other`
- `tests/test_shared_homes.py::test_the_waiting_lock_hardens_its_file_before_it_locks_and_returns_the_holder`
- `tests/test_shared_homes.py::test_a_held_lock_shuts_out_a_second_holder_until_the_body_ends`
- `tests/test_jobs.py::test_reconcile_leaves_a_genuinely_running_job_alone`
- `tests/test_jobs.py::test_a_running_job_is_never_listed_for_cancel_however_old`
- `tests/test_jobs.py::test_a_second_driver_refuses_while_a_live_holder_has_the_lock`
- `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
- `tests/test_jobs.py::test_resuming_a_job_a_live_driver_already_holds_refuses_in_the_foreground`

So the guard is held, by the tests that name it, and the row is read as killed
by hand, not by the driver. Unmodified, the same two files pass.
