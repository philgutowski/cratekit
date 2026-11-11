---
title: A file that reaches the staging folder while a label go's tail runs lands with the go
found: at the review of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** A go reads the folder before its tail and refuses beside
anything that is not its own; the tail itself does not read it again
between `name apply` and `intake land`. A download that commits into the
folder while the tail analyses is landed with the go under its manifest and
pass. Its record (`keep_tail`) leaves out a track another download recorded
at its download name, but a file no job records, such as a Bandcamp sync's,
which records no artifact, or a file a person drops in, is kept as the go's
own and read so on the next go under its run.

**Measured cost.** Driven at the review's round two (`test_cr.py::test_cr3`)
by committing a plain download inside the analyze step: the landing argv was
the go's, over the go's tracks and the plain one. The producer, a second
process downloading into staging during a tail, was not driven.

**Closes when:** the landing's own plan is checked against the go's tracks
before its gate, or the tail reads the folder again before the landing.
Ledger only: the producer is a concurrent second verb, unmeasured.
