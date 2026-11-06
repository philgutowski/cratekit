---
title: A stopped write's carried record stays on disk for good when its pair is unpaired or never synced on both sides again
found: at the build of #591, R-1372, 2026-11-06.
issue: no
---

**The mechanism.** R-1372 lets a carried record go when its own run marks the pair done, or when a snapshot of the pair taken after it is recorded. A pair unpaired after a stop, or synced only on one side from then on, never reaches either, and nothing ages the record out, by design, since a stop must be remembered while its pair is unfinished. An unreadable carried record is likewise named on every gate until it is removed by hand.

**Measured cost.** Not driven as a cost: each record is a small file, read by nothing once the pair's mark is later than its write (`_Reader.stopped_write`'s mark guard). An unreadable one says so on every gate, which is noise rather than a wrong write.

**Closes when:** forgetting or releasing a pair lets go of its carried records, and a verb or a doctor check offers to clear one that cannot be read.
