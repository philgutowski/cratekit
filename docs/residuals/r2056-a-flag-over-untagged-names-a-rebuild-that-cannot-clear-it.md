---
title: A flagged routing tree whose only differences are untagged keeps its flag, and its refusal still says to run the rebuild
found: at the review of #1061, R-2056, 2026-11-24.
issue: no
---

**The mechanism.** A rebuild clears a tree's unconverged flag only when its after check converges, and an `untagged` vocal membership is a difference the additive rebuild cannot remove. `assert_converged`'s refusal (`tree-unconverged`) gives the step "run the rebuild for this tree", and `accept_as_it_stands` refuses a derivable tree. So a tree flagged by a restore whose remaining differences are untagged vocal memberships stays flagged until each is tagged or taken out, and the refusal does not say so.

**Measured cost.** Driven by the review on a disposable database: tagged, rebuilt, the association marked removed, the tree marked unconverged; the rebuild job exits 0 with the `vocal-membership-untagged` warning, the flag stays, and `route inbox` refuses with the rebuild step. The same holds before this branch for any `unexpected` leftover, the 484 on the live library among them, so R-2056 does not change whether the live tree clears today. The out of band restore detection that sets the flag was not driven.

**Closes when:** the unconverged refusal names, beside the rebuild, what a rebuild cannot settle (the leftovers and the untagged, taken out or tagged) when the last check found them. Ledger only: maintainer wording over a state that already existed.
