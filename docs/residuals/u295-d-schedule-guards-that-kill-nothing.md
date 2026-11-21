---
title: Several of the schedule's guards kill no test
found: at the review of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** Round two's 48 rows over the fix's guards in `src/cratekit/cli/schedule.py` found 15 with zero deaths. Mended in fix round two: words after `sync night` on the reading side, a relative log, the minute range and the type check of the calendar. Still killing nothing on the round's own reading: the environment shape check in `read_agent`; `_boot_out` returning `state == LOADED` alone or `out.ok` alone; the write failure message saying the earlier schedule is off whether or not one was booted out; `replaced = had_plist` alone; the launchctl timeout's value (the hang test sets its own); and `settle` dropped from `show`'s night line.

**Measured cost.** None today: each is a guard whose removal no test notices. The unit's own table, `docs/mutation/u295.md`, measures the 25 rows it ranked above these.

**Closes when:** each has a test that dies when it is removed, or the record says why it need not.
