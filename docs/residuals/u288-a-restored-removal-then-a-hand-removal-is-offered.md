---
title: A removal restored and then removed again by hand in rekordbox is offered by delete review from the old record
found: at the review of #839, U288, round one, 2026-11-21.
issue: no
---

**The mechanism.** `recorded_removals` reads every standing record of the
database and skips a row the database holds again. After a restore puts the
row back, the record still stands; when the person later removes the same
track by hand in rekordbox, the row is absent again and the old record offers
its file, at the old record's sequence if the watermark is still below it.

**Measured cost.** Driven by round one: after the restore, offered 0; after a
hand delete, offered 1. The offer is behind `delete.review.confirm` and its
proofs, and a hand removal is a removal, so the cost is a file offered that
the person did mean to remove; the GUIDE now says so.

**Closes when:** a restore marks the removal records it reaches back past as
undone, or the pass reads a record only for rows it removed after the last
restore. Ledger only.
