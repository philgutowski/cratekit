---
title: A session log path under a regular file reads as no log at all, where U214's probe read it as unlisted
found: at the review of #526, R-1255, 2026-11-05.
issue: no
---

**The mechanism.** `session._listed` answers `None` for a log path whose
parent is a file (`NotADirectoryError` with nothing at the path), so
`scan_log` answers no record and nothing unread, and every gate reads a
library with no session. U214's probe in the rotation, which R-1255 replaced
with the scan's own, answered it as unlisted, so the rotation's warning on
that shape is lost. The choice is pinned by
`test_a_log_under_a_file_is_not_there`.

**Measured cost.** Driven on the branch: the four readers answer as for an
absent log. No verb puts a file at the state root, so it is reachable only by
hand, and nobody was found to pay for it.

**Closes when:** a state root replaced by a file is decided to be a refusal
of its own, upstream of the session log, or the trade stays as recorded.
