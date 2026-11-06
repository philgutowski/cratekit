---
title: A mirror job whose source playlist the mirror record no longer names lifts nothing, with no word on the plan
found: at the review of #594, U230, 2026-11-06.
issue: no
---

**The mechanism.** `account_mirror._read_edits` maps each job's source remote
identifier to a title through the playlists the mirror record holds now
(`titled`). A playlist retired and made again under a new identifier since
the queue maps to nothing, so its base is not lifted, and the plan says
nothing of the unmapped source.

**Measured cost.** Read, not driven. The edit is read as U227 reads it.

**Closes when:** an unmapped source is named on the plan, or mapped by title.
Ledger only.
