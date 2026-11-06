---
title: Two of R-1349's tests list the readers of an open gate by hand and author the unreached run they drive
found: at the review of #574, R-1349, 2026-11-06.
issue: no
---

**The mechanism.** `test_the_refusal_is_not_an_open_gate_to_any_reader` in
`tests/test_gate_not_reached.py` checks four readers, the reason, the remedy
token, `render.is_gate_screen` and the exit code, by name; a fifth reader of an
open gate added later is not covered. And
`test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen`
makes its unreached state by clearing a `profile set` run's offer and open gate
by hand, a state the test authors rather than one a verb produced. The organize
drives in `tests/test_organize.py` carry the real producer.

**Measured cost.** None: round one's grep found no reader of
`decision-required` or `ExitCode.DECISION_REQUIRED` outside the four modules
the test covers, and the dispatcher test checks only the human text.

**Closes when:** the readers are enumerated from the tree, and the dispatcher
drive reaches its unreached gate through a verb with two digest gates. Ledger
only, maintainer facing.
