---
title: A new row can still pass as a replay by naming a recorded source and writing a moved reason
found: at the review of #854, U297, round two, 2026-11-21.
issue: no
---

**The mechanism.** A replay pass has no row cap because every row names a
recorded kill. `scripts/mutate.py` reads each source before anything runs:
the table exists under `docs/mutation/`, holds that row, the row recorded a
death, and a row whose file or text is not its source's must carry a `moved`
reason. A row anchored again by hand is exactly that, so the reason cannot be
refused, and nothing ties the new text to the old guard but the author's
word, which is committed in the table.

**Measured cost.** The review drove 26 new rows under real sources with no
reason, which is now refused. With a reason on each they would be measured.
Maintainer facing, and it takes an author writing 26 false reasons into a
committed table.

**Closes when:** it is accepted as the limit of a text based check, or
`killset.py check` is made the only reader of a replay table and holds a row
at new text to a test in common whoever wrote its reason. Ledger only.
