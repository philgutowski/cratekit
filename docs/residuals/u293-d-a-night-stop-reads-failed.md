---
title: A night pass stopped at its line reads failed, not blocked
found: at the review of #850, U293, 2026-11-21, round one finding 12.
issue: no
---

**The mechanism.** The dispatcher reads a park as blocked for the ceiling and the hour's budget only, so a night pass stopped by `provider-night-budget` ends with outcome `failed` and exit 42, where a pass meant to wait would read blocked.

**Measured cost.** None on the night's own record or line, which say stopped and that the next night continues it. A wrapper reading the envelope's outcome, the U295 schedule's log above all, reads a failure.

**Closes when:** the dispatcher reads the night's park as blocked, like the hour's.
