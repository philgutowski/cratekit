---
title: the favorites step skipped warning reads every item the drive did not find done, and counting a done one too kills no test
found: at the review of #1036, R-2020, 2026-11-24.
issue: no
---

**The mechanism.** `rebuild.ReportedDrive.of` reads `driven`, the trees this
run drives, as every item not yet done, and only the favorites step skipped
warning (U132) reads it. The round one review changed the filter to keep every
item, done or not, and no test died; the base's two resumes read the same
filter and had the same gap.

**Measured cost.** None measured: a job continued with a tree already done and
a taxonomy whose favorites class is missing would name that done tree's skipped
step again, which is true of the tree and only says it twice. Not driven.

**Closes when:** a resume over a job with one tree done and one pending, under a
taxonomy with no favorites class, asserts the warning names only the pending
tree. Ledger only.
