---
title: a plain crate sync land after a pass stopped at its landing gate ends no_op while the staged tracks wait
found: at the review of #333, U152, 2026-10-28.
issue: no
---

**The mechanism.** A pass that reached the landing's gate leaves its intake jobs succeeded and its tracks staged. A second `crate sync land` with no `--pass-run` runs `sync all`, which finds nothing new, and with no intake job open the pass ends `no_op`, saying nothing of the staged tracks or of the landing still waiting on its gate.

**Measured cost.** Driven at the first review. The first pass's pending envelope named the gate run and the commands that answer and apply it, so the person holds the way on; the second answer is silent rather than false.

**Closes when:** a pass with nothing new reads the staging folder or the open landing gate and names it. Ledger only.
