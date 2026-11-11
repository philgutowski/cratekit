---
title: A label go reads every item of every job in the queue before its gate and before every tail
found: at the review of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** `label.go.beside`, and `keep_tail` after the tail, read
every job's item rows, any handler, to find the downloads with a track in the
staging folder; the handler filter was dropped so a fallback fetch's track is
read. A queue with many large jobs (tag and analysis jobs carry one item a
file) is read in full each time.

**Measured cost.** Measured at the review's round two (`test_misc.py::test_p1`):
40 jobs of 5,000 items, 0.81 to 0.90 seconds over 3 repeats, against 0.001
seconds with none. The live queue's size was not measured.

**Closes when:** the read asks the store for done items whose artifact sits
under the staging folder in one query. Ledger only.
