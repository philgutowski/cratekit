---
title: "A file's inode under the cloud container's temp directory can fall below the repair bound, so an inode test reddens the mutation baseline with nothing changed"
date: 2026-11-01
category: workflow-issues
module: "tests/test_repair_rows.py, scripts/mutate.py, scripts/cloud_battery.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: environment_dependency
resolution_type: workflow_improvement
applies_when:
  - "scripts/mutate.py refuses a red baseline in a cloud session and names a test the branch never touched"
  - "A test reads a file's st_ino and compares it with a fixed bound"
symptoms:
  - "BASELINE IS NOT GREEN: 1 failing, naming test_an_id_above_the_bound_that_is_the_files_inode_is_not_random"
  - "The same test passed in cloud_battery.py baseline and compare an hour earlier on the same container"
  - "It fails alone, every time, with within_bound 3 where 2 is expected"
tags:
  - "cloud-lane"
  - "mutation-driver"
  - "inode"
  - "ext4"
  - "intermittent"
  - "linux"
---

# A file's inode under the cloud container's temp directory can fall below the repair bound

## What happened

U180's mutation run was refused before any row ran: its baseline named
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
a test of the row repair the branch never touched. It had passed in the
battery's baseline and compare on the same container earlier the same hour,
and it failed alone three times in a row.

## Why

The test makes a file under pytest's temp directory and expects its inode to
be above the repair's 2,000,000 bound, as it is on a volume whose counter has
run past it, the Mac's case. On the container's ext4 root, a file under
`/tmp` was handed inode 615,346 at the time, below the bound, so the file
read as within the bound. ext4 picks an inode from the parent directory's
block group, so the number depends on where the temp directory sits and on
what the allocator has freed since, which is why the battery passed and the
driver, an hour later, did not.

## What to do

Read a fresh file's inode under `/tmp` (`stat -c %i`). If it is below
2,000,000, give the run a temp directory in a top level directory, which ext4
spreads to another block group with high inodes: `mkdir /mtprobe` then run
the driver with `TMPDIR=/mtprobe`. The test then passes alone, the baseline is
green, and nothing in the suite or the baseline file was edited. Never add
the test to `.cloud-battery/baseline.txt` by hand.

## Since U273

The battery names this test on its `ON_DISK` list. `cloud_battery.py
baseline --temp memory` runs the suite on the memory filesystem, where a
file's inode is in the thousands and the test always fails, then runs the
listed tests again on disk, and their disk outcome is the one recorded; the
driver does the same for any run that collects them. Measured on 2026-11-13:
run alone on the container's disk the test failed 4 of 4 times, a fresh
file under `/tmp` getting inode 620,000 or so; it passes in a full run on
disk only after the run has written gigabytes. So the battery's default stays
disk while Phillip decides (#702), and with `--temp memory` this test reads
as the machine's in both the baseline and the compare.
