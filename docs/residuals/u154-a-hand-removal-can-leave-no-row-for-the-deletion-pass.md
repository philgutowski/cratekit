---
title: A row removed through rekordbox's dialog can leave no row at all, and the deletion pass, which reads the soft delete marker, never offers its file
found: at sitting 45, 2026-10-27, the attended session after U154 (#335).
issue: no
---

**The mechanism.** `deletion.library.read_collection` finds a removal by
`rb_local_deleted`, the marker the first live removal was seen to set (the
learning "the first removal is a soft delete"). The 36 rows sitting 29 removed
through rekordbox's own dialog on 2026-10-02 hold no row in the live database
in either state, while the 7,404 soft deleted rows baselined at sitting 9
still stand. Which removals rekordbox hard deletes and which it marks is not
known; what is known is that both happen in this library. A file whose row is
gone outright is invisible to `delete review`, so it stays on disk with
nothing pointing at it and nothing offering it, and a batch holding one cannot
be shelved, since `intake shelve` leaves a batch whole when a file has no row.

**Measured cost.** `delete review` over the 36, owed since sitting 29, would
have offered none of them even with a complete reference set; it refused
before that on the 153 unmapped rows of R-675. The 36 files, 919 MB, were
moved by hand at sitting 45 to `Removed_from_collection/2026-10-01-labels-1pct`
at the volume root for Phillip to trash, and the batch was shelved after.

**Closes when:** the deletion pass also offers a file under a batch folder that
no row references at all, under the same inode and size proof `candidates`
already makes, or the record states that a hand removal's file is trashed by
hand. Ledger only.
