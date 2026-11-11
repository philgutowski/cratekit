---
title: A label go's run names the landing its tail reached for ever, after that landing was applied, aborted or went stale
found: at the review of #647, U239, 2026-11-10.
issue: no
---

**The mechanism.** U239 records the landing run a go's tail stopped at on the
run whose go queued the job (`landing_role` in `src/cratekit/label/go.py`),
and a later `--go` under that run names it and runs nothing. The record is
never cleared, so after that landing is applied, aborted or refused stale the
go still names it, and the way to run the tail again is by hand.

**Measured cost.** Not driven: the suite's stand in landing has no real run.
Nothing is written over; the person is pointed at a spent run.

**Closes when:** the continuation reads the named run's state and, when its
gate was aborted or its plan went stale, runs the tail again. Ledger only.
