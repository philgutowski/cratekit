---
title: A generation restarted by the stream measures again what it has not been asked for, and nothing tests that it skips what was read
found: at the review of #649, U241, 2026-11-11.
issue: no
---

**The mechanism.** `WorkStream._start` hands a generation only the positions
not yet read (`if position not in self._read`). The review changed it to hand
out every position and no test failed. The guard matters only when a reader
goes back to an earlier generation, which `analyze run` never does: it reads
in item order.

**Measured cost.** None reachable from the shipped verb. With the guard gone,
a reader that went back would have an item measured twice, time only, and the
second result unread.

**Closes when:** a stream test reads a later generation and returns to an
earlier one, counting what each child measured. The author could not kill it:
the row was the review's, measured at zero. Round two also noted that
`light.longest_seconds` has no caller left under `src` since the cost became
the costliest track's, and that the warm up's twelve seconds can fall to two
with its coverage test still passing, which the comment now says. Ledger
only.
