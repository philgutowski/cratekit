---
title: The test that captures every behaviour scenario twice takes about sixteen seconds, and grows with every scenario an area card adds
found: at the build of #854, U297, 2026-11-21.
issue: no
---

**The mechanism.**
`tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
runs `scripts/behaviour_compare.py capture` twice as two real processes over
every file under `tests/behaviour/` and compares the two. It is the one test
that goes red when a scenario prints or writes something the stage did not
pin. One capture of the six shipped scenarios is about eight seconds, most of
it the scenario run's own start up and the 152 help screens.

**Measured cost.** 15.5 and 16.5 seconds in two runs on the four core cloud
container, of a suite that sums to about 1,870 seconds of test time, so under
one percent, and real work: two child runs of pytest. It is over METHOD's ten
second line for a slow test, and each area card under U290 adds its verbs'
scenarios to it, while U312 has to make the suite 30 percent faster.

**Closes when:** U312 decides it: the equality is held over a fixed sample
of scenarios in the suite and over all of them by each card's own capture,
or the two captures share one scenario run. Ledger only.
