---
title: analyze check calls a grid variable when any one beat differs by a hundredth
found: at the review of #348, U167, 2026-10-31.
issue: no
---

**The mechanism.** `rekordbox_check.read_grid` reads a grid as constant only
when every beat carries the same tempo in hundredths. One beat at 128.01 among
128.00 makes it variable and the visit suspect, exit 27, "the widest moving
0.01".

**Measured cost.** Unmeasured: whether rekordbox's Normal analysis ever writes
such a grid has not been read off a real file, since the container holds none
and pyrekordbox ships no sample. If it does, every such track reads suspect.

**Closes when:** the attended visit reads real Normal grids and either
confirms they carry one value or sets a tolerance from what they carry. Ledger
only.
