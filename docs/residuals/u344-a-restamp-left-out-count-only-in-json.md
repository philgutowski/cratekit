---
title: In the default output a restamp told a run's job never says what it left out, and its no op reads as an empty folder's
found: at the review of #996, U344, round one, 2026-11-23.
issue: no
---

**The mechanism.** `analyze restamp --scored-by RUN_JOB_ID` counts the files
it left out at `progress.left_out` in its queue answer and at
`progress.analysis.left_out` in its job answer. The default renderer prints
neither, so a person reading the plain answer sees `items: 1 of 1 settled`
with no count and no reason, and when the run scored every file the answer
is `analyze.restamp: no_op`, the same words an empty folder gives.

**Measured cost.** Driven by the review through `drive_human` over the
suite's fixtures. The tail reads the JSON answer and says the count on its
own `restamp` row, so a sync pass is not affected; only a person running
the flag by hand reads less than the answer holds.

**Closes when:** the default output names the count and the run job, and
the no op says the run scored every file. Ledger only.
