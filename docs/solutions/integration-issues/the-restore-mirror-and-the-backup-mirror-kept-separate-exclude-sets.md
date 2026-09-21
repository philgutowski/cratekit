---
title: "The restore mirror and the backup mirror kept separate exclude sets, and the fake remote ignored both"
date: 2026-09-21
category: integration-issues
module: cratekit.modules.tools.backup
problem_type: integration_issue
component: restore
severity: medium
root_cause: inconsistent_contract
resolution_type: code_fix
tags: [restore, bare-metal, rclone, exclude, fake-remote, r-592]
applies_when:
  - "A guard's safety argument rests on what the restore mirror does or does not land"
  - "Changing the exclude patterns on any rclone command in backup.py"
  - "Writing a test against the bare metal verb's fake remote"
---

# The restore mirror and the backup mirror kept separate exclude sets

## Problem

R-592 narrowed the bare metal occupancy guard to the fileset where this
library's database lands, on the argument that the mirror never writes there.
The BACKUP mirror excludes that fileset, `backup._mirror_excludes`. The RESTORE
mirror, planned in `_plan_restore_inside_the_gates`, passed only
`VOLUME_EXCLUDES`. So a remote mirror taken before the backup excluded the
database could still land it at the landing path, and the argument held only
for remotes written after that exclusion existed.

## Why the suite could not see it

The verb suite's fake remote, `_Remote` in `tests/test_restore_cli.py`, wrote
every file in `mirrored` whatever the argv excluded. Any change to the restore
mirror's excludes, in either direction, was invisible to it. The built in review
found the gap by reading, not a test.

## Fix

The restore mirror passes `_mirror_excludes(cfg)`, the backup's own set, so
the two cannot disagree about the database. `_Remote` now honours an anchored
`--exclude /path` the way rclone does, and
`test_a_mirror_still_carrying_the_database_does_not_land_it` drives a stale
mirror that holds `db/master.db`. Mutation row B6 of `docs/mutation/r592-b.md`
reverts the excludes and is killed.

## Watch for

The share snapshot command beside it still passes `VOLUME_EXCLUDES` on purpose,
because the share is not the library root. A sed that rewrites every
`_exclude_args(VOLUME_EXCLUDES)` in `backup.py` catches it too, which happened
once while measuring this.
