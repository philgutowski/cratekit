---
title: A head measured again in the driver while the workers run is one worker's memory the plan did not count
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** When a head measured ahead cannot be used, because its
file changed or a worker raised on it, `analysis/ahead.py` measures it in the
driver by the serial line. The workers are still running, so for the length
of that one track the run holds one more light worker's memory than
`light.plan` afforded.

**Measured cost.** Not observed: both paths need a file swapped during a run
or a file the detector raises on, and the plan keeps a quarter to a half of
the budget as headroom. A pool that broke or was stopped has no workers, so
the common fallback costs nothing extra.

**Closes when:** the session pauses its workers, or reads one fewer result
ahead, while the driver measures. Ledger only.
