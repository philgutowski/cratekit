---
title: A bootout that answers a failure after an unreadable first print is counted as nothing booted out
found: at the review of #852, U295, 2026-11-21.
issue: no
---

**The mechanism.** `_boot_out` in `src/cratekit/cli/schedule.py` counts an agent booted out only when launchd read it loaded first or the bootout answered success. When the first `launchctl print` cannot be read, the bootout answers a failure and launchd then reads the agent absent, `remove` answers no op and a failed install's refusal omits that the earlier schedule is gone.

**Measured cost.** Eight of 1,088 stood in launchd answer combinations at round two, one shape. Not driven against a real launchctl, and whether launchd produces that sequence is unknown.

**Closes when:** the ambiguous case is said as such in the report rather than counted either way.
