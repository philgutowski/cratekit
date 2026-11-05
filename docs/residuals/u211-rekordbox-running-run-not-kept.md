---
title: A gated write refused because rekordbox opened ends failed, though its answers are kept and --run continues it
found: at the build of #505, U211, 2026-11-05.
issue: no
---

**The mechanism.** U211 keeps the run of a refusal under
`rekordbox-absence-unconfirmed` (`cli.gates.KEPT_RUN_REASONS`): resumable,
blocked, and naming `crate --run RUN ...`. A refusal under `rekordbox-running`
at the same guard, a person launching rekordbox between the gates and the
write, is left as it was: outcome failed, `resumable` false, no continue
step. The answers given with `crate run decide` are on the run's record
either way, so `--run` does continue it; only the envelope does not say so.

**Measured cost.** Not driven against a person. `tests/test_process_scan.py`
pins the narrow set, so widening it is a decision rather than a drift.

**Closes when:** Phillip decides whether a refusal for a running rekordbox at
a gated write should keep its run the way an unconfirmed absence does, and
the set is widened or left. Ledger only.
