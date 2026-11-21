---
title: One file whose name holds a line break or carriage return makes every backup a full check, however little changed
found: at the round two review of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** rclone reads a quick run's paths one per line, so the walk
refuses a name holding a line feed or a carriage return, and a refused walk is
a full run that keeps no record. macOS's folder icon file, `Icon` followed by a
carriage return, is such a name, and it never changes, so every run is full.

**Measured cost.** Driven on three consecutive days: full each day with
`backup-record-not-kept`. The card's measure of minutes is never met on a
library holding one. Whether the live library holds one is unmeasured; the
attended card runs a `find` for it first.

**Closes when:** such a name is carried by the full check alone and left out
of the record and the comparison, so a quick run neither lists it nor reads
its absence as a removal, or the walk excludes `Icon\r` as volume clutter.
Ledger only.
