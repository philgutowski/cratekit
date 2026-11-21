---
title: When a removal gives the deletion pass its first position, the first delete review never says how many removals it accepted as history
found: at the review of #839, U288, round two, 2026-11-21.
issue: no
---

**The mechanism.** A first `delete review` that baselines shows `baselined`
and `accepted_as_history` so a person learns the history before now was
accepted (R35, R-134). When `sync removed` gives the position instead, it
drops the store's `(mark, baselined)` answer and says nothing, and the first
review then shows `baselined: false, accepted_as_history: 0`.

**Measured cost.** Driven by round two with one marked row and no position:
the notice is never shown anywhere. Not reached on Phillip's library, which
holds a position since 2026-09-23.

**Closes when:** the removal's envelope names the position it gave and how many
marked removals it accepted as history. Ledger only.
