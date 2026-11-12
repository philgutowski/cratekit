---
title: The sweep's call estimate does not count the release a sweep re-verifies, one provider read a label and two after a gone answer
found: at the build of #777, R-1634, 2026-11-12.
issue: no
---

**The mechanism.** Since R-1634 the one held release a sweep verifies again,
when a release it turned down came back with no label credit, is always read
from the provider (`reread_release`), one call a label, and a second when
the first answers that the provider no longer has it. U278's estimate before
`label sync --next` without `--label` counts a kept listing's answers and
not this read.

**Measured cost.** Not driven against a budget. At most two calls a label
on the refusal path, against a read line of 1,125 and an estimate U278
already records as counting answers and not pages.

**Closes when:** the estimate counts one call a label whose listing turned
everything down, or the estimate is replaced by a measured spend. Ledger
only.
