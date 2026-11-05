---
title: Session release clears the stale lock before it reads the log again, so a listing refused in between reports a refusal over a lock already cleared
found: at the review of #526, R-1255, 2026-11-05.
issue: no
---

**The mechanism.** `crate session release` reads the session log through
`session.records` before its question, and again after `release_stale_lock`
has cleared the lock, to abandon orphans and list what is kept. Since R-1255
that reader refuses an unlisted log, so a log that becomes unlisted between
the question and the answer ends the run refused with the lock already gone.

**Measured cost.** Not driven. Nothing in the tool changes the log's mode
inside the verb; it needs a person or another account to do it in that
window. The lock cleared is the one the person asked to clear.

**Closes when:** the release reads the log once more before clearing the
lock, or the envelope says the lock was cleared when the later read refuses.
