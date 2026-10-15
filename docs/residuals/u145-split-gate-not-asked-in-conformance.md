---
title: The month split's approval gate is exempt from the conformance drive, since the fixture cannot write and a library with no quarter asks nothing
found: at the build of #324, U145, 2026-10-15.
issue: no
---

**The mechanism.** Conformance 3 drives every verb's gates on one shared
fixture and asserts OK after the two acts. `favorites.split.approve` is asked
only over a library holding a quarter playlist, and approving it writes, which
that fixture refuses for its unpinned rekordbox (S2). The brief says a library
with no quarter opens no gate. So the gate joined `UNREACHABLE_GATES` and
`EXPECTED_UNREACHABLE_GATES`, the fifth exemption, decided here unattended.

**Measured cost.** Maintainer facing. The verb's own suite drives the gate's
two acts, its refusals and the write in `tests/test_favorites_split.py`.

**Closes when:** the conformance fixture can make a database write, a pin
recorded for its drive alone, at which point the sample makes an empty
quarter and the exemption is deleted. Ledger only.
