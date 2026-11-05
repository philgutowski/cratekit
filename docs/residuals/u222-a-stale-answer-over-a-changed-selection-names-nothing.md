---
title: A stale account answer over a changed --only selection says every step plans as the gate showed it and names no mover
found: at the review of #552, U222, round two, 2026-11-05.
issue: no
---

**The mechanism.** The account area's digest covers its `--only` selection as
well as its steps (`Area.identity`), but `mirror_frozen.moved` compares the
steps alone. A resume whose selection differs from the gate's, with the same
steps, is refused stale, and U222's lines say "every step plans as the gate
showed it" beside "a plan that has since changed", without naming the
selection that moved.

**Measured cost.** Driven through the dispatcher at round two: a gate on the
mirror kind alone, `run decide`, a resume naming the mirror and `marks`; exit
11 with that line, nothing asked and nothing written. The refusal is correct
and the replan works; the cost is a naming gap.

**Closes when:** the frozen plan carries the gate's selection and the stale
lines name a selection that differs. Ledger only.
