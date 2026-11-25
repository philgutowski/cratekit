---
title: crate status reads every run record twice, and each call of it adds one
found: at review round one of #1079, U960, 2026-11-25.
issue: no
---

**The mechanism.** `crate status` lists and loads every run record for its
own run lines (`doctor._run_report`) and again for the glance
(`status_glance.gate_runs`), and the dispatcher saves a run record for every
verb, `status` included, so an app that polls the verb grows the directory
it reads by one record a call.

**Measured cost.** At 20,000 records, three repeats on the cloud container:
the glance's scan 0.65 to 0.88 seconds, `_run_report` 0.66 to 0.73, the
whole verb 1.39 to 1.54. At 200 records the verb answered in 0.40 to 0.69.
An app polling once a minute adds 1,440 records a day; the count on
Phillip's machine is unmeasured.

**Closes when:** the status verb loads the records once and hands them to
both readers, and the menu bar app's card decides whether its polling verb
records a run at all. Ledger only.
