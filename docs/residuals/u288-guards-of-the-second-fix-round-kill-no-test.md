---
title: The rule that picks the first deletion position and the removed count in restore's refusal kill no test
found: at the review of #839, U288, round two, 2026-11-21.
issue: no
---

**The mechanism.** Round two mutated `max(counter, highest)` to the counter
alone, and `highest` to the counter, and deleted restore's `, N removed`
suffix: each killed none of the tests that cover them, since no test puts a
marked row above the counter or refuses a restore over a removal session.

**Measured cost.** None to a person today: the rule is the pass's own, and the
suffix reads right when called directly. Maintainer facing.

**Closes when:** a test holds a marked row above the counter to the position,
and one holds restore's refusal over a removal session to its removed count.
Ledger only.
