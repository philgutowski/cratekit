---
title: The repair rows test of an inode above the bound passes or fails on a Linux container by the inode its temporary file is given
found: at the mutation table of #604, R-1394, 2026-11-07.
issue: no
---

**The mechanism.** `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`
writes a temporary file and records its real `st_ino` as the row's file id,
then asserts the plan counts it within the bound. On this cloud container
the test passed alone once and failed alone the next run, with no change to
the tree, so its result follows the inode the filesystem hands out rather
than the code. The base's measured baseline did not catch it red, so the
mutation driver refused its first baseline over it. R-1372's landing met
the same test newly failing in its compare.

**Measured cost.** Maintainer facing: a cloud battery or mutation baseline
reddened by a test none of the branch's files reach, costing a rerun. Not
driven on a Mac, where the volume's counter may keep it steady.

**Closes when:** the test gives its file an inode it controls, or reads the
bound from the volume it writes to, so its result no longer depends on the
container. Ledger only.
