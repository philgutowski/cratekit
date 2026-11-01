---
title: Ctrl-C on a foreground tail drive says nothing until the item in hand finishes
found: at the review of #403, U192, 2026-11-01.
issue: no
---

**The mechanism.** `jobs.interruptible` records the signal and the drive honours it only between items, by design, so nothing is half written. U192 makes the drive the default answer of `tag folder`, `analyze run` and `analyze restamp` run by hand, so a person now presses Ctrl-C at a terminal holding a drive, and the verb prints nothing until the item it is working on ends.

**Measured cost.** Driven by the review: a handler that slept 1.5 seconds after the signal returned 1.51 seconds later, the job queued again and its `--job` command named. On a long analysis decode the wait is the length of one track's work, and the press reads as ignored until then. The answer that follows is true.

**Closes when:** the engine's signal handler writes one line, that the run will stop after the current item, the first time it records a signal. Ledger only.
