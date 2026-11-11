---
title: An analyze run stopped with Ctrl-C carries its pool in the refusal's detail and not in what the person reads
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** A run that fails leaves through its cause, and U241
appends the pool's sentence to the cause's steps and its record to the
detail. A run stopped in the foreground then passes through
`modules/foreground._resumable`, which replaces the steps with its own two,
the resume command and the count of settled items, so the pool's sentence is
dropped there and only `detail.pool` survives. The resume that finishes the
job prints the line as a check.

**Measured cost.** A person who stops a run does not see how many workers it
had until they resume it; `--output json` shows it at once. Driven by
`test_an_interrupt_during_a_run_ahead_ends_the_workers_and_the_resume_finishes`,
which reads the detail.

**Closes when:** `_resumable` keeps the steps a cause already carried after
its own two, for every queued verb, which is a change to the shared
foreground and so not this unit's. Ledger only.
