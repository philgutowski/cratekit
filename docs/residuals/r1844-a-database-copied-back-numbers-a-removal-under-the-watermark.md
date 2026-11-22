---
title: A database copied back by hand puts the update count under the deletion watermark, so a later outright removal is numbered under the position and never offered
found: at the review of #926, R-1844, round two, 2026-11-22.
issue: no
---

**The mechanism.** An absent landed row is numbered by the update count at the
first run that sees it gone (`deletion.watermark.WatermarkStore.sight`, R-1037),
and offered only when that number is past the watermark's position. A database
put back by hand, or by a bare metal recovery from an older snapshot, brings back
an older and lower update count, while the watermark document, which lives
beside the library, keeps its later position. A row of a standing landing that is
removed afterwards is numbered at the lower count, under the position, and never
offered. `crate restore run` restores the watermark with the database, since it
is COUPLED state, so it is not affected.

**Measured cost.** Driven by round two's review on a disposable library: land,
baseline, land two more, copy the database, move the count up by 500, remove and
trash a track (watermark 713), write the copy back (count 213), and remove a
landed track outright. It is numbered at 213 and nothing is offered, and the file
is kept. This was already true on main before #926, which changes neither the
numbering nor the filter.

**Closes when:** the pass notices an update count lower than the watermark's
position for the same database and says so, or numbers from the higher of the
two, with a test of a hand copy back. Ledger only: the cost is a kept file, and
the producer is a hand copy or a bare metal recovery, not a Cratekit verb.
