---
title: Full suite baselines fail under parallel load on tests no card owns, so a kill set replay cannot run side by side on one container
found: at the kill set replay of #867, U310, 2026-11-22.
issue: no
---

**The mechanism.** A replay batch runs the whole suite twice before its first
row, the baseline and the null control, and refuses the batch on any death.
With three batches and four build workers on one four core container, five
tests outside adopt and deletion failed one baseline or control each and
passed alone: `tests/test_jobs.py::test_two_processes_claiming_the_same_job_never_claim_one_item_twice`,
`tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`,
`tests/test_rb_writer_guard.py::test_second_writer_refuses_while_lock_held`,
and the two inode bound tests in `tests/test_repair_rows.py`, the first of
which also failed alone in a clone under the temporary directory (#702).
Each refusal came after an hour of baselines, and two batches were then cut
at the two hour limit with about fifteen rows measured each.

**Measured cost.** About five hours of replay time on this card, and the
before batches moved to helper containers. The replays read a scratch copy of
the measured known failures naming these five, the same file before and
after; the measured `.cloud-battery/baseline.txt` was never edited.

**Closes when:** the three load sensitive tests wait on an event rather than
on time, or a replay batch on a shared container is documented as one at a
time. Ledger only.
