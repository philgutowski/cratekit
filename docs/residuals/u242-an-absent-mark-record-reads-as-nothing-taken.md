---
title: An absent mark record reads as nothing taken, so once the prefix is stripped a lost sync_marks.json offers every stripped playlist as new
found: at the review of #671, U242, round one, 2026-11-12.
issue: no
---

**The mechanism.** `MarkRecord._read` answers empty lists when
`sync_marks.json` does not exist, which is right for a library that never
marked anything and was right before U242, when a lost record cost only the
undo. Since U242 the record is the only thing that holds a stripped playlist
as taken, and an unreadable record refuses while an absent one reads as none.
The review drove it: strip, delete the file, and `sync all` queued the
stripped playlist as new.

**Measured cost.** Every playlist the strip took the prefix off would be
offered and queued as intake. No product verb deletes the record, which is
`NEVER_RESTORED` so a database restore leaves it alone; 0 producers of an
absent record were driven, so the reachability is unmeasured.

**Closes when:** the record states that a strip ran, in a place its own
absence cannot erase (the library's state index or the cursor's document), so
an absent record after a strip refuses rather than reading as empty. Ledger
only.
