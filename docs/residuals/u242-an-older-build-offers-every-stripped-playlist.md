---
title: A build older than U242 offers every stripped playlist and refuses the version 2 mark record, so the live strip waits for every installed copy
found: at the review of #671, U242, round one, 2026-11-12.
issue: no
---

**The mechanism.** A build before U242 knows a taken playlist only by its
`DOWNLOADED ` title, and reads the mark record only at version 1. The review
drove `origin/main`'s source against a stripped title and a version 2
document: its `exclusion` returned nothing for the title, so a sync there
would offer it, and its `MarkRecord` refused the document ("it says version 2
and this build writes 1").

**Measured cost.** On an installed copy that lags behind U242, every playlist
the strip took the prefix off is offered as new, and every mark verb refuses
the record. Not driven as an install; the attended card owed by U242 updates
the installed copy before the strip.

**Closes when:** the strip has run only on installations that carry U242,
which the attended card's first step makes true. Ledger only.
