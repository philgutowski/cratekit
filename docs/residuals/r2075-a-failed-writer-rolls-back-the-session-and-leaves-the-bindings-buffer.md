---
title: A failed writer rolls back the session and leaves the binding's update buffer, so a later commit on the handle bumps the update count for rows that never landed
found: at the review of #1077, R-2075, 2026-11-25.
issue: no
---

**The mechanism.** `trees.rollback_quietly` in `src/cratekit/write/trees.py` calls `db.session.rollback()` and never the binding's own `db.rollback()`, which also clears pyrekordbox's process wide update buffer. After a failed native landing the buffer still holds the landing's creations and updates, and the binding's `commit` raises `agentRegistry.localUpdateCount` by one per buffered entry before it commits. The native landing, analyzed, refill, rotate, set_playlist and shelve all unwind through it.

**Measured cost.** Not driven to a user. The round one review drove the C11 test's shape on the disposable copy: after the landing failed, a later `db.commit()` on the same handle landed no row and no playlist, but moved the update count from 100 to 137 (the binding's commit refusing) and from 100 to 131 (a failure before the guard); with `db.rollback()` in its place the buffer read 0 and the count did not move. No caller commits on a handle after a failed write: the three `apply_rows` callers raise, and `open_db` clears the buffer for the next handle. A count rekordbox reads as other changes than there were is the cost, should one ever do so.

**Closes when:** the quiet rollback clears the binding's buffer as well (its own `rollback`, or `rb_changes.clear_registry_buffer` beside the session's), and the C11 test in `tests/test_intake_land_native.py` also asserts the update count is unchanged after the later commit. Ledger only: no reachable producer.
