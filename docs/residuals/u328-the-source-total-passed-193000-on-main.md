---
title: The source total passed 193,000 lines on main while the further cards of U290 built, by feature cards
found: at the build of #977, U328, 2026-11-23.
issue: no
---

**The mechanism.** Point 2 of #847, U290, asks that `src/cratekit` outside
`_vendor` end at or under 193,000 lines. The final audit (#872, U315) read
188,904 on `d289f61` and held that half of the point. Feature cards kept
landing while the further cards built, and nothing in the battery holds the
total, so it grew past the bar under a green suite.

**Measured cost.** `scripts/refactor_measure.py lines`, and `wc` over the
tracked files for the earlier commits: 188,904 at `d289f61`, 190,196 at
`392a2d1`, 191,607 at `4d1ff8b9`, 191,899 at `c84dc4ac`, 192,016 at
`99e0cbc0` and 193,136 at `2e8681d1`, all on 2026-11-23, then 193,253 at
`e0573a66` and 193,382 at `c5fb1015`, the base U328 merged on. U328's
split of the verb table adds 107 more, the five parts' heads and the
assembly, so the head it merged reads 193,489, 489 over. None to a person using a verb.

**Closes when:** the audit card of #847, #987 (U338), measures point 2 again
and files a further card for the total, or Phillip moves the bar for the
features added since. Ledger only: a maintainer facing count.
