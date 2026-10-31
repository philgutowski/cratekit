---
title: Two of the pending object sources the DEADCA7 guard reads kill no test, each covered by the other
found: at the review of #392, U185, 2026-10-31.
issue: no
---

**The mechanism.** `rb_writer.pending_objects` unions the binding's update buffer and the session's pending collections, as `pending_changes` does. Dropping the buffer's `move` branch, or the `session.dirty` loop, leaves every U185 test green, because the other source reports the same object for each touch the tests make, and the second reading from SQL catches whatever is flushed.

**Measured cost.** None to a person: the guard still refuses every touch the review drove. Measured as zero death rows in the review's mutation pass.

**Closes when:** a test drives a touch only one source reports, a write the binding does with its tracking disabled for the session side, and a raw session change for the buffer side. Ledger only.
