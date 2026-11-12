---
title: The organize run that shows a gate and writes nothing still opens the database once per reading step
found: at the build of #696, U267, 2026-11-12.
issue: no
---

**The mechanism.** U267 shares one read handle across `crate organize
--report` only. The run that plans both areas and stops at the first gate
writes nothing either, and the run that answers rebuilds the plan again, but
both take the same code path as the run that writes, so the brief kept them
on an open per reader: the `world` fixture's answered run made 26 opens on
the base and makes 26 now, 20 of them the three planning passes' reads.

**Measured cost.** Not driven on the real library. On the container an open
of an encrypted fixture database was measured at 165 ms by the speed survey,
and A124 measured an open of the real database at 0.27 s cold and 0.07 s
warm, so each planning pass spends about half a second to a second and a half
on opens.

**Closes when:** a card shares one read handle across a run's planning, read
only up to the gate, with every write still opening its own, or a measurement
on the Mac shows the cost is not worth a card. Ledger only; the brief put the
gated runs out of scope.
