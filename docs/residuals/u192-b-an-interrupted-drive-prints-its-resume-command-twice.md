---
title: An interrupted tail verb prints its resume command twice, as the fix line and as the first step
found: at the review of #403, U192, 2026-11-01.
issue: no
---

**The mechanism.** `modules.foreground` rebuilds the cancelled refusal with no remedy token and the `--job` command as its first step. `render.remediation_line` falls back to the first step for every refusal with no token, and `render_cause` then lists every step, so the human answer reads `fix: resume it with: crate ... --job ID` and the same sentence again under it.

**Measured cost.** Driven by the review with `crate tag folder` interrupted: the two lines are identical and both true. Nothing is false, only repeated.

**Closes when:** `render_cause` skips the first step when the fix line already printed it, for every remedy-less refusal. Ledger only, a wording fix.
