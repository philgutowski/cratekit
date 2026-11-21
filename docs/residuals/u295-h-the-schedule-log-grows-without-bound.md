---
title: The scheduled night's log grows without bound
found: at the plan of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** launchd appends the agent's output and errors to `schedule/sync-night.log` under the installation's state (`schedule_log`) every night, and nothing rotates or trims it.

**Measured cost.** Not measured. A night's output is a few lines when the pass refuses and a pass's whole report when it runs, so the file grows by kilobytes a night.

**Closes when:** the log is trimmed or rotated, or the record measures that it need not be.
