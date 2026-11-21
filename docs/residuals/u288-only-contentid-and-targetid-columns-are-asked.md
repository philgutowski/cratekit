---
title: The removal asks other tables only by columns named ContentID and TargetID, and TargetID without the table it names
found: at the review of #839, U288, round two, 2026-11-21.
issue: no
---

**The mechanism.** `rb_writer.content_references` refuses a track any table
outside the removal set names by `ContentID`, or by `TargetID`. A table naming
a track by another column (`ContentID1`, `ContentUUID`, `TargetUUID`) is not
asked, so its row would be left naming a deleted track; and a `TargetID`
naming a row of another table that happens to equal a content id keeps the
track for the wrong reason.

**Measured cost.** Driven by round two on synthetic tables: a
`djmdRecommendLike (ContentID1, ContentID2)` row was left naming the removed
track, and an `imageFile` row for a playlist kept a track forever. Neither the
repository nor the binding names such a table, and whether the live schema
holds one is unmeasured.

**Closes when:** the live schema is read for every column that can name a
content row, each asked, and `TargetID` asked with its `TableName` where the
table has one. Ledger only.
