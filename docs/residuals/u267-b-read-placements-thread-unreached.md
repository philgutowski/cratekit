---
title: The shared read handed to the adoption plan's placements reader is reached by no report
found: at the review of #696, U267, 2026-11-12.
issue: no
---

**The mechanism.** U267 threads `one_read` through `apply_cli.current_plan`
into both of its tree readers, `placements.read_holdings` and
`placements.read_placements`. Organize plans the adoption with `vocals` left
true, so only `read_holdings` is reached; `read_placements` is reached only by
`current_plan(vocals=False)`, whose one caller, the move verb
(`adopt/move_cli.py`), passes no shared read. The thread was kept so the two
branches of `current_plan` read alike.

**Measured cost.** None. Found by grep in the review, and a probe over every
report the organize suites drive saw no report reach it; no test drives the
parameter there, so a mutation of it would read zero.

**Closes when:** a report that plans without vocals is built and a test
drives the shared read through `read_placements`, or the parameter is
removed from that reader. Ledger only.
