---
title: The toggle scenario's last loop runs five verbs with every toggle on
found: at the review of #860, U303, 2026-11-22.
issue: no
---

**The mechanism.** `tests/behaviour/cli.py`
`test_every_toggle_off_and_a_missing_extra` reads every toggle off through the
real parser and keeps the verbs each preset lists, which is what the
comparison holds. Its last loop then runs help and one verb of five modules
named by hand, with no toggle turned off, so the five imports U303 moved
inside functions are driven through a real verb only with their toggles on.

**Measured cost.** None: turning a toggle off removes verbs from the parser
and uninstalls nothing, and the review found no reachable difference.

**Closes when:** the loop writes a configuration with each toggle off and
runs the remaining verbs, or is dropped as covered by the parser reading.
Ledger only.
