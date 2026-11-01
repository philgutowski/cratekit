---
title: A tail step stopped at a gate other than the landing's names the answer as the literal word OPTION
found: at the review of #401, U190, 2026-11-01.
issue: no
---

**The mechanism.** `cratekit.cli.tail.attended` fills the option of `crate run
decide` with `apply` only for the landing's gate, and with the placeholder
`OPTION` for any other, so a person told to answer a tail step's own gate is
handed a command that cannot be pasted as printed. The options are in the
step's cause detail and are not read.

**Measured cost.** Driven at the stand in: a `analyze restamp` queue command
answering `decision-required` on its own gate produced `crate run decide
restamp-run analyze.restamp.confirm OPTION --actor session`. No landed tail
verb was found to raise a gate of its own at that step, so the producer is
unmeasured. The wording is U152's, moved here unchanged.

**Closes when:** the step names the gate's declared options from the cause
detail, one command per option or the one a session takes, with a test.
Ledger only, since the producer was not driven.
