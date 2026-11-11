---
title: A label go whose tail left no record refuses its own go over its own renamed tracks
found: at the review of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** A run's own `--go` reads a file no download names as its
own only when its tail's record (`label.go.keep_tail`, kept by the CLI layer
whichever way the tail ends) names it by name, size and modification time.
No record is kept when the process dies mid tail, when the record cannot be
written (a warning), for a go whose tail ran under a build before R-1467, or
when a person edits a renamed track's tags before the go is run again. The
go then refuses its own tail beside its own renamed tracks.

**Measured cost.** Driven at the review's round two (`test_misc.py::test_u1`,
the record stripped as an earlier build leaves it): exit 42, the two renamed
tracks named as tracks no download names, no tail run. The refusal names the
tail by hand, which lands them; nothing is lost. A go in flight across the
upgrade is the reachable producer; its count on the live store is unmeasured.

**Closes when:** a go that finds files no download names and no record of
its own tail can tell its renamed tracks by something that survives (the tags
the tail wrote), or the refusal says plainly that they may be its own.
Ledger only: the way on is named and works.
