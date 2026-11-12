---
title: The cloud battery's reporting plugin writes on the xdist controller only, and nothing tests that guard
found: at the review of #697, U268, 2026-11-12.
issue: no
---

**The mechanism.** `PLUGIN_SOURCE` in `scripts/cloud_battery.py` returns early
on an xdist worker (`hasattr(config, "workerinput")`), so only the controller
writes the run's report. Removing the guard leaves every test green: xdist
workers call `pytest_terminal_summary` inside their own session finish, before
they report themselves finished, so the controller always writes last and
overwrites any worker's partial report. The review drove it with a probe
plugin (each worker wrote first, the controller last) and removed the guard
against both test files (all passed).

**Measured cost.** None today: the mutant reaches no wrong result, and if a
worker's partial report were ever the one left, its counts would disagree with
the summary line and the run would be refused, never read. It is the same
shape as the mutation driver's own controller only write guard, R-1574.

**Closes when:** a test runs a suite where the controller's write could come
before a worker's, or the guard is accepted as equivalent. Ledger only.
