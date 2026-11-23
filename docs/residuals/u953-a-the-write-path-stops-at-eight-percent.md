---
title: The write path's code lines fall 8 percent under U953, not 15, and its fifteen test files stay above their line target
found: at the build of #953, U953, 2026-11-23.
issue: no
---

**The mechanism.** #953 (R-1887) asked the write path's 27 files to fall from
9,287 code lines to 7,688 or fewer, and the fifteen test files #857 lists to
10,655 lines or fewer, with behaviour frozen. Measured by
`scripts/refactor_measure.py lines` on the merged head, the code is at 8,549
(7.9 percent fewer) and the tests at 11,562 lines (3.7 percent fewer); their
summed test time, the third target, is met (23.9 and 26.7 seconds on the base
with two workers, 11.8 and 13.5 on the branch). Five builders cut disjoint
files and each stopped at the same floor: every `__all__` nothing read, every
re-export nothing reads through its facade, the dead names, and every
repeated refusal and parallel branch were folded, and what is left is
distinct message text, cause detail and guards, which only reflowing lines
would shorten, and the brief puts reflowing out of scope. In the tests, about
2,800 of the remaining lines are blank separators inside tests and 800 are
docstrings.

**Measured cost.** None to a person using the verbs: the behaviour comparison
over 215 scenarios shows no difference. Point 4 of #847's definition of done
reads short for this area, for the audit #872 to weigh.

**Closes when:** Phillip settles the question on #953 (recommended: land with
the miss named and no further card for the same count), or a later card finds
a simplification these five did not. Ledger only: maintainer facing, not on
the board bar.
