---
title: The done verdict of analyze check has no behaviour scenario, since reaching it needs a beat grid file on disk
found: at the build of #863, U306, 2026-11-22.
issue: no
---

**The mechanism.** `tests/behaviour/analysis_check.py` drives `crate analyze
check` to waiting (exit 12), suspect (exit 27), the fallback scope, nothing in
scope and its refusals. The done verdict (exit 0) needs an analysis file that
holds a readable grid, which no scenario may write under the standing rule
against beat grids. Patching the grid reader would reach it, but a patch that
stops biting after a later move would read as a false difference.

**Measured cost.** None today: the verdict's code is covered by
`tests/test_analyze_check.py`. The behaviour comparison cannot see a change to
what the done verdict prints.

**Closes when:** a scenario reaches the done verdict through a fake the
product itself reads at call time, kept where the reader lives. Ledger only.
