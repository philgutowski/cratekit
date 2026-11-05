---
title: The snapshot pruner reads the session log through a glob of its own, so an unlisted log protects no snapshot
found: at the build of #526, R-1255, 2026-11-05.
issue: no
---

**The mechanism.** `rb_writer.read_run_state_records` globs the run state
directory and `default_protected_snapshot_paths` builds on it, so a log this
account cannot list yields no record and protects no capture from
`rb_writer.prune_snapshots` or from `restore.retention_plan`'s default
provider. R-1255 moved `session.scan_log` off its glob and left this second
reader of the same directory on one. `restore.prune` with no owning session
refuses first since R-1255, through the reporting reader; with one named it
does not read the log and reaches the provider.

**Measured cost.** Not driven. Neither `rb_writer.prune_snapshots` nor
`restore.prune` has a caller in `src`, so no person pays for it today.

**Closes when:** the pruner reads the log through `session.scan_log` and
refuses on an unlisted one, before any verb prunes with the default
protection.
