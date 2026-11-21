---
title: A delete made on the raw session and flushed before the commit reaches neither source the whitelist reads, so it commits
found: at the review of #839, U288, round one, 2026-11-21.
issue: no
---

**The mechanism.** `pending_changes` reads the session's pending collections
and the binding's update buffer. `db.delete` reaches the buffer; a
`session.delete(row)` followed by a flush leaves `session.deleted` empty and
never reaches the buffer, so `commit_guarded` with no `deletions` commits it.
Predates U288, whose own deletes go through the binding and whose
confinement reads every table from SQL.

**Measured cost.** Driven by round one on a disposable copy: the content row
was deleted by a commit that named nothing. No producer: `session.delete(`
has no hit under `src`.

**Closes when:** the whitelist also compares a reading from SQL before and
after for every commit, or a source guard refuses `session.delete` outside the
writer. Ledger only.
