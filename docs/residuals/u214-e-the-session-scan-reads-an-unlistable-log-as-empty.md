---
title: The session scan reads a log directory it cannot list as no record and no unreadable one, for every consumer but the rotation's classifier
found: at round two of the review of #512, U214, 2026-11-05.
issue: yes
---

**The mechanism.** `session.scan_log` globs the log directory, and a glob over
a directory the account cannot list yields nothing rather than raising, so it
returns `(), ()`: no record read and none unreadable. U214 made the rotation's
classifier ask the listing itself (`rotate.Landings.unlisted`), so its
unrecognised reason says the log could not be listed. Every other consumer of
`scan_log` still reads the unlistable log as empty, the gates included, and the
rotation's own `rotate-records-unreadable` warning does not fire on it, so a
batch recognised by its name rather than its record is aged from its playlist's
creation date with no warning.

**Measured cost.** Driven at the review as an unprivileged account with the
log directory's mode set to none: the scan answered no record and no unreadable
one, and nothing warned. The producer was a permission change made outside the
tool, so the natural producer is unmeasured; the repository treats a directory
it cannot list as a reachable class. A gate that reads the log through the
scan fails open on it, which the scan's own docstring names as the shape it
exists to prevent.

**Closes when:** `scan_log` asks the listing and reports an unlistable log as
unread, each gate consumer refuses on it, and the rotation warns on it as it
warns on an unreadable record. Earns an issue under the board bar's (b) and
(d): a clean report over state it could not read, and a guard on a gated path
that reads unread as none.
