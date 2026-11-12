---
title: U264's two review rounds ran on Opus 5.5 with Fable out of usage, and owe a Fable pass
found: at the review of #693, U264, 2026-11-12.
issue: no
---

**The mechanism.** Both of U264's review rounds were refused by Fable on its
usage limit and ran the `fable-reviewer` definition on Opus 5.5 at high
effort instead, as the cloud-unit skill's Models section allows when Fable
is out of usage.

**Measured cost.** None measured; a review by a different model may miss
what Fable would have found.

**Closes when:** Fable reviews the merged range of U264 (the merge commit's
first parent to the merge) against the merge bar. Ledger only.
