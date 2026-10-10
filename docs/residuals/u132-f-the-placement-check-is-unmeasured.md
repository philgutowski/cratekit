---
title: The upgrade's check that an added block left every entry whole is unmeasured
found: at the mutation table of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** `_placed` in `core/taxonomy_upgrade.py` inserts an added
class or bucket before the copy's entry that follows it in shipped order, then
keeps the result only if `_kept_whole` finds every entry the copy held exactly
as it was. Turning that check off kills no test (P9), and the composite meant
to show what it holds (P9_composite, the placement one line later) kills none
either, because the following entry's span starts at its comment run and the
shifted block lands between two comment lines, which parses the same.

**Measured cost.** A placement that breaks the parse is still refused by the
candidate load (P3, killed) and by the tests that parse the result back. What
is unguarded by any test is a placement that parses and loads but moves keys
from one entry into the added one. The placement code computes its index from
the same block scan the cut uses, and no copy in the suite, the live one
included, drives it wrong.

**Closes when:** a test hands `_placed` a copy whose following entry has no
comment run and checks that a shifted index is refused, and a table measures
P9 against it. Ledger only.
