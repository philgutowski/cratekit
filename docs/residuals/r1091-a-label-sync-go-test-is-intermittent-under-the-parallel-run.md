---
title: The label sync go test of a tail run in order fails intermittently under the full parallel suite since U186 landed
found: at the battery of #410, R-1091, 2026-11-01.
issue: no
---

**The mechanism.** `test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
in `tests/test_label_sync_go.py` fails in some full parallel runs of the
suite on the Linux container and passes alone, with its whole file, and with
every `tests/test_label_*.py` file under all workers. It first appeared once
U186 (`tests/test_gate_siblings.py` and the gate's sibling reads) was on
`main`, in R-1103's battery and twice in R-1091's, and passed in R-1091's
third full run on the same head. The failing assertion was not captured, since
`cloud_battery.py compare` keeps node ids only, so which shared state it meets
is unmeasured.

**Measured cost.** Maintainer facing: a cloud lane's compare names it as
newly failing, and each lane spends a rerun proving it is not its own. No
user facing cost was found or driven.

**Closes when:** a full parallel run captures its traceback, the shared state
it reads under load is named, and the test or the code it drives no longer
depends on it.
