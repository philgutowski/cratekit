---
title: The restore session's unconfirmed absence at its database half carries both the continue step and the conditional remove step
found: at the review of #505, U211, 2026-11-05.
issue: no
---

**The mechanism.** `session/restore_cli._absence_unconfirmed` ends the scan's
refusal on the rerun step every database half failure carries ("remove
master.db and any companion if one is there"), and the dispatcher keeps the
run and puts the continue command first. A process that turns unreadable
between the session's own scan and the database half shows four steps, two of
which say how to go on.

**Measured cost.** Driven by the round one review: mirror landed, database not
attempted, detail `half=database, completed_halves=[mirror]`, four steps.
Nothing is false, since the remove step is conditional and nothing landed; the
list is longer than it needs to be.

**Closes when:** a kept refusal at the database half carries only the
continue step, or the two are made one sentence. Ledger only.
