---
title: U306 left tagging, analysis and vocals short of their line, code line and test targets, and with eleven seam lines other cards own
found: at the landing of #863, U306, 2026-11-22.
issue: no
---

**The mechanism.** #863's brief set, for the 40 source files and 36 test
files of `tagging`, `analysis` and `vocals`, at most 17,444 source lines,
10,189 code lines, 23,357 test lines and 30 percent less test time. Measured
on the merged head by `scripts/refactor_measure.py lines` against the base
`c9192091`: source 23,494 to 18,785, code lines 13,104 to 12,718, test lines
31,668 to 29,619, and the test time not told apart on this container. No file is over
1,500 lines and no copied block is left. The code that remains is mostly code
the recorded kill set finds by its exact text, so cutting it means rewriting
guarded code with every replayed row re-anchored by hand, which this card did
not do. Eleven import allowance lines stay because the modules they name are
another card's: `core.art` and `core.taxonomy_word` from tagging and
`core.cores`, `core.discovery`, `core.drift`, `core.pool` from analysis, and
`core.discovery` from vocals, all core modules off the interface list, which
is full at 25 and which U301 (#858), merged in before this card landed, left
as it was; the registry loading `analysis.check_cli` for a verb the analysis
toggle does not gate (#860, U303); and vocals importing `analysis.artifacts`,
`analysis.cli` and `analysis.vocals` at top level, which a lazy import would
change for a person running the vocals verb with analysis off.

**Measured cost.** None to a person: behaviour is unchanged. The cost is to
#847's definition of done, points 2, 4 and 5, which the final audit measures.

**Closes when:** the final audit, #872 (U315), measures the epic and files a
further card for the gap, as #847 says a point that falls short gets. Ledger
only.
