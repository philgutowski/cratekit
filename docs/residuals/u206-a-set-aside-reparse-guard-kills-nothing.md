---
title: The ISRC cache's re-read under the lock before a set aside kills no test
found: at the review of #496, U206, 2026-11-05.
issue: no
---

**The mechanism.** `Cache._set_aside_held` in `src/cratekit/acquire/isrc_cache.py`
reads the file again under the lock and renames it aside only if it still does
not parse, so a good file another process wrote between this process's read and
its lock is never set aside on an old reading. Replacing it with a rename that
skips the re-read killed none of 153 tests (Fable round one, in process).

**Measured cost.** None driven. The race it covers, a second writer landing a
good file inside that window, was not produced. If it happened without the
guard, the cost is calls, never data: the good file is set aside and rebuilt.

**Closes when:** a two process test lands a good file between the read and the
lock and shows it kept. Ledger only.
