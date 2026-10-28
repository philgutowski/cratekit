---
title: U166 was reviewed by the reviewer agent on Opus, not Fable, which had reached its usage limit
found: at the review of #347, U166, 2026-10-28.
issue: no
---

**The mechanism.** The cloud lane's rule is that Fable at high effort
reviews every unit. Both of U166's review rounds were refused by the Fable
limit on this account (HTTP 429, "You've reached your Fable limit"), so the
same `fable-reviewer` agent definition was run with the Opus model instead,
the conservative call that keeps the lane moving rather than holding a built
unit for an unknown time.

**Measured cost.** Unmeasured: no independent review of the same branch by
Fable exists to compare. The Opus round one found and drove one BLOCKING
finding and six residuals, so the round was not empty.

**Closes when:** Phillip asks for a Fable pass over the merged range, or says
the substitution stands for a unit that meets this limit. Ledger only.
