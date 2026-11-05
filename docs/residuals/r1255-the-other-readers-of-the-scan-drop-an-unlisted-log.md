---
title: The scan's readers that drop its unread half by their own policy drop an unlisted log with it, unsaid
found: at the review of #526, R-1255, 2026-11-05.
issue: no
---

**The mechanism.** `account_mirror.landed_tracks`, `pair_cli`, the set
export, `set_playlist._landed` and `account_playlists.mirrored` and
`pending_names` read `session.scan_log` and keep only the parsed half, a
policy each chose for one damaged record. An unlisted log arrives in that half
and is dropped too, so each reads it as a log with no record and says
nothing. `unread_clause` also words a regular file standing at the log path
as a log "this account cannot list", whose remedy is a permission, where the
file needs replacing.

**Measured cost.** Not driven. Every one of these that feeds a write runs
inside `assert_gates`, which refuses an unlisted log first since R-1255, so
the cost is a report or a plan that is quiet about a log nobody read.

**Closes when:** each reader that reports says the log could not be listed,
as the rotation, the refill and the check do since R-1255, and the clause
names a file at the log path as one.
