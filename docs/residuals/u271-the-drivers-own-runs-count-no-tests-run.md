---
title: The mutation driver's own runs count no tests run, so a run that stopped early with no failure reads as complete
found: at review round two of #700, U271, 2026-11-13.
issue: no
---

**The mechanism.** U271 taught the cloud battery to count every test that
reported and the driver to refuse a battery record whose count of tests run
differs from its collected count. The driver's own plugin in
`scripts/mutate.py` (`PLUGIN_SOURCE`, read by `run_pytest`) counts what was
collected and what failed, and nothing that ran, so a run of its own that
stopped early with tests unrun, and no failure among those that did run,
would read as green. Since U271 the null control is the only full run in the
driver's own environment whenever the full baseline is read, so it carries
more weight than it did.

**Measured cost.** Not driven to a cost. Round two drove three candidates and
none produces an early stopped run with no failure: `pytest.exit` under the
repository's xdist exits 3, which `run_pytest` raises as a measurement
failure; `-x` arrives only through `PYTEST_ADDOPTS`, which the driver scrubs,
and stops on a failure, which is a death; a worker crash with its restarts
spent files the crash as a failure. Predates U271.

**Closes when:** the driver's plugin counts the node ids that reported, as the
battery's does, and `run_pytest` raises a measurement failure when that count
differs from the collected count. Ledger only.
