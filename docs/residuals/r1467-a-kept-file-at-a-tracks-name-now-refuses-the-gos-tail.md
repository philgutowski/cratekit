---
title: A label go whose track is refused output-exists now refuses its tail until the file kept at that name is moved
found: at the build of #655, R-1467, 2026-11-11.
issue: no
---

**The mechanism.** R-1115 landed the rest of a go's download when one track
failed for good with `output-exists`, a file already at the name it lands
under. That file is not the go's download, so since R-1467 the go refuses
before its gate while it is in the folder, and refuses its tail if it
appears during the download, naming it as a track no download names. The
four R-1115 tests that produced the failure with such a file now keep it in
the folder only while the drive runs, so they pin how such a download
settles, not a state a person reaches.

**Measured cost.** Driven at the review's round two (`test_oe.py`) with the
file left in place: exit 42, the tail not run, the refused track and the
kept file named. A person moves or lands the kept file, then runs the go
under its run again. Nothing lands under the wrong pass.

**Closes when:** a test reaches a download failed only for good by a
producer that leaves nothing in the folder, or the R-1115 reading is
restated over the refusal. Ledger only.
