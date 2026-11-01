---
title: "An inode bound test passes once on the Linux container, so the base battery misses it and the mutation driver's null control dies"
date: 2026-10-28
category: workflow-issues
module: "tests/test_repair_rows.py, scripts/cloud_battery.py, scripts/mutate.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: environment_constraint
resolution_type: workflow_improvement
applies_when:
  - "scripts/mutate.py reports INVALID BATCH: the null control killed 1, naming test_an_id_above_the_bound_that_is_the_files_inode_is_not_random"
  - "a test fails alone on the cloud container while .cloud-battery/baseline.txt does not list it"
tags: [cloud, mutation, null-control, baseline, inode, linux, repair-rows]
---

## The trap

`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`
expects a freshly made file's inode to be above `row_defaults`' bound of
2,000,000, which holds on the Mac's APFS volume, whose counter has run past
it. The cloud container's ext4 hands out inodes around 400,000 to 700,000, so
the test fails there. But not every time: measured on the base commit
`3d94634` on 2026-10-28, run alone four times, the first fresh run passed (in
75 seconds) and the next three failed in two seconds.

`scripts/cloud_battery.py baseline` caught a passing run, so the id is not in
`.cloud-battery/baseline.txt`, and `scripts/mutate.py` then saw it fail under
its semantically empty null control, twice, and refused both batches as
INVALID. Nothing in the unit's diff touches it.

## What to do

- Run it alone on the BASE commit (check the base out in the same checkout on
  a clean tree, run it four times, check the branch out again). Failing there
  makes it the machine's, whatever the baseline file says.
- Do not write the id into `.cloud-battery/baseline.txt`, which is measured.
  Copy that file to the scratchpad, append the id with the measurement as a
  `#` comment, and pass the copy to `--known-failures`. Say so in the table's
  notes, as `docs/mutation/u166-notes.md` does.
- A clean rerun of `cloud_battery.py baseline` may catch it passing again, so
  rerunning the baseline is not the fix.
- Or point the driver's temporary directory at `/var/tmp`, measured by R-1032
  on 2026-11-01: the same ext4 volume hands a file made under `/var/tmp` an
  inode near 9,700,000, above the bound, where `/tmp`, `/root` and the
  checkout gave 400,000 to 650,000. `TMPDIR=/var/tmp/<unit> scripts/mutate.py
  ...` then ran a green baseline and a zero null control with no copy of the
  baseline file at all, and the test's file passed 53 of 53 there.
  It changes where the suite writes, never what it asserts.
