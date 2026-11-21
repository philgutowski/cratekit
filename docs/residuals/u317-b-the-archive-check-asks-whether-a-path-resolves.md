---
title: A quick run's archive check asks whether a removed path resolves, so a case only rename on a Mac volume fails the run and costs a full check
found: at the round two review of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** `backup_record.still_removed` refuses the archive when a
path the walk found removed resolves with `lstat`. On a case insensitive
volume a case only rename (`Album/a.flac` to `Album/A.flac`) leaves the old
spelling resolving, and a folder replaced by a symbolic link leaves its old
paths resolving through the link, so the quick run fails with "was found
removed by the walk and is there again" and the next run is a full check.

**Measured cost.** The symbolic link case was driven: one failed run, then a
full check, no age or file wrong. The case only rename was emulated, since no
case insensitive file system mounts in the container. Each costs a failed
backup and one full run, never a wrong skip or a lost file.

**Closes when:** the check compares the path as the walk would list it, by
the exact name in its directory's listing and not by resolving it. Ledger
only; the attended timing card renames one folder by case to measure it.
