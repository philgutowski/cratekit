---
title: U290's point 2 is short at its last measurement, src/cratekit at 195,379 lines against 193,000 and write/rebuild.py at 1,517 against 1,500
found: at the build of #987, U338, the last measurement of U290 (#847), 2026-11-25.
issue: no
---

**The mechanism.** Point 2 of #847's definition of done: `src/cratekit` outside `_vendor` at or under 193,000 lines, and no source file over 1,500. Measured by `scripts/refactor_measure.py table` and `lines --files` on `main` at `147574d`: **195,379 lines in 413 files**, 2,379 over the bar, and **one file over 1,500, `src/cratekit/write/rebuild.py` at 1,517**. U315 read 188,904 lines and `cli/registry.py` at 2,491 on `d289f61`; U328 took the registry under 1,500. Since `d289f61` the source grew by 6,475 lines. By the numstat of the commits in `d289f61..147574d` over Python files outside `_vendor`, renames followed, grouped by the unit their subjects name (6,479 in all, 4 more than the tree, not traced further), the epic's further cards added 156 net (U328 107, U331 84, U329 minus 35), and feature cards outside the epic 6,323, the largest U339 1,413, U958 1,229 and U340 1,109; `write/rebuild.py` crossed 1,500 by R-2056 and R-2062, a crossing R-2034 foresaw: no battery check holds the 1,500 line bar on a source file. R-2037 recorded the total passing 193,000 while the further cards built and closes on this measurement; this entry carries the shortfall from here.

**Measured cost.** Maintainer facing: the size the refactor was asked to reach is not where `main` stands. No verb's behaviour is affected.

**Closes when:** `refactor_measure.py table` reads at most 193,000 lines and 0 files over 1,500, or Phillip retires the bar. By Phillip's decision of 2026-11-24 on #847, no further area card is filed for it. Ledger only.
