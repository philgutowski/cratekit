---
title: A continue of a refused order that is not a finish writes rekordbox's order over a reorder a person made on the account between the two commands
found: at the review of #613, R-1411, 2026-11-07.
issue: yes
---

**The mechanism.** Pre-existing, from U220, and not changed by R-1411. For
an order that is not a finish and was refused once, a continue of the run
passes as `expect` the continue's check listing, which the check judges for
what it holds and not its order (`_beyond(ordering=True)` in
`sync/pair_cli.py`). A person's reorder on the account between the refusal
and the continue passes the check and is the reading expected, so the
continue writes rekordbox's order over it.

**Measured cost.** Driven by round two on a scratch copy: the `owed` world
(rekordbox 4, 3, 1, 2), the order refused once `read-differs`, the person
setting the account to 2, 4, 1, 3, then `crate --run RUN sync pair`: exit 0,
reported written, the account 4, 3, 1, 2 and the person's order lost. A
fresh sync over the same two reorders takes the account's order into
rekordbox instead. It needs a refusal and a hand reorder between two
commands of one run.

**Closes when:** a continue's check judges the order of a pair whose order
was refused against the plan's reading, and holds the pair as moved when a
person changed it. Earns an issue: a person's hand reorder on the account is
lost under a clean report.
