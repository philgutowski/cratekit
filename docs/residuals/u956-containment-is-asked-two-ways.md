---
title: Adoption asks whether a file is inside the library root one way, and the tree writer resolves it another
found: at the review of #1020, U956, 2026-11-23.
issue: no
---

**The mechanism.** `cratekit.adopt.scan.within_root` decides by name on whole
components, then asks each parent whether it is the root (`os.path.samefile`).
`cratekit.write.trees.index_active_rows` groups rows by the text their recorded
location resolves to through the prefix rules. Two shapes fall between them.
A prefix rule whose target is a link, outside the root, to a folder under it
(`root/Music`) reads `outside-root`, so a real library file is named as not the
library's and left out. A rule whose target is another name for the root
itself passes the samefile walk, so the row routes, and the membership write,
which matches by text, cannot place it: the pass fails `adopt-entries-failed`,
with a refusal step ("two live rows for it or none") true of neither case.

**Measured cost.** Driven by the round one reviewer with both rules written by
hand. Neither is a regression: the base fails both passes. Setup's rule offer
was not driven, and a case folding volume, the shape the samefile walk is
there for, cannot be driven on Linux.

**Closes when:** the census and the tree writer read containment and identity
through one resolution, so a row the census routes is one the writer can
place, with a test for each shape above. Ledger only: no input a person makes
through the shipped verbs was shown to produce either.
