---
title: The tail's run, through the name step and then the landing, has no caller left
found: at the review of #665, R-1499, round two, 2026-11-11.
issue: no
---

**The mechanism.** `crate sync land` and `label sync --go` now call `tail.through_name`, compare the folder, then `tail.land`; `tail.run` is still exported and one test exercises it.

**Measured cost.** None; a maintainer facing function no verb calls.

**Closes when:** `tail.run` is removed or reads the folder between its two halves itself. Ledger only.
