---
title: Verifying a kept release with no copyright line reads its album again, which the listing line does not count
found: at the review of #533, U217, round two, 2026-11-05.
issue: no
---

**The mechanism.** `TidalCatalogue.search_release` reads a release's album
again when the listed object carries no copyright line. A kept release keeps
the line it was listed with, so one listed bare is read again on every run,
and that read is verification's, outside the listing's count. Round two found
the listing line said "with no provider call" over it; the fix round reworded
it to "with no listing call to the provider", which is true.

**Measured cost.** Driven by the review on the suite's stand in client, whose
listed albums carried no copyright line: two album reads on the second run.
The same reads happen on `main`. Whether a live listing ever omits the line was
not driven.

**Closes when:** the album's answer is kept with the release, or the verb's
line also counts verification's reads. Ledger only.
