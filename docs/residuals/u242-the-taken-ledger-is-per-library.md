---
title: The taken ledger is kept per library while the account is the installation's, so a second library syncing the same account would offer every stripped playlist as new
found: at the build of #671, U242, 2026-11-12.
issue: no
---

**The mechanism.** The taken ledger lives in the sync marks record, which is
library state (`StateRoot.LIBRARY`), as the playlists cursor and the mark
record always were. Before U242 a prefixed title excluded a playlist on every
library, because the title is the account's. After `crate sync strip` takes
the prefix off, only the record of the library the migration and the strip
ran on holds those playlists as taken. A second library on the same
installation, syncing the same account, whose record never had `crate sync
taken` run against it, would read each stripped playlist as new and `sync all`
would queue it as intake.

**Measured cost.** Not driven: no fixture here makes a second library over one
account, and whether any installation does is not known from the repository.
The attended card owed by U242 runs the migration on every library before the
strip, which closes it for the live account.

**Closes when:** the ledger is keyed by the account rather than the library,
or `crate sync strip` refuses while any library this installation knows has
not recorded the prefixed playlists. Ledger only.
