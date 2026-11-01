---
title: Two sync land tests each reddened the mutation driver's whole suite baseline once and pass alone, in their file's parallel run and in the battery
found: at the mutation table of #379, U182, 2026-11-01.
issue: no
---

**The mechanism.** Measuring U182's table on the Linux container, the driver refused a red baseline twice, each time over one test of `tests/test_sync_land.py`: `test_a_fresh_pass_never_reuses_another_lists_download_job` under the null control, then `test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`. Each passed six times alone, the file passed three times under `-n auto`, and two full battery runs on the same heads counted neither. The third driver run was green.

**Measured cost.** Two driver runs of about fifteen minutes each spent. No product cost: the tests drive stand ins, and no cause was measured. Whether U182's new read in the left open row takes part was not measured; neither test asserts on that row.

**Closes when:** the failure is caught with its traceback, by running the driver's own command until it reddens, and its cause is named. Ledger only, maintainer facing.
