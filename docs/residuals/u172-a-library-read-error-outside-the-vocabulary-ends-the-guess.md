---
title: tag guess reads an unreadable library as a warning only when the error is Cratekit's own, so a bare database error would end the pass at its guess step
found: at the review of #353, U172, 2026-11-01.
issue: no
---

**The mechanism.** `tagging.guess_cli._library` opens the database to read and walks its rows inside a `try` that catches `CratekitError` only. A locked or half written database that raised a bare sqlite or SQLAlchemy error while the rows are walked would escape as `internal-error`, and the tail ends the pass at the guess step rather than guessing from the folder and the playlists.

**Measured cost.** One candidate was driven, a database file of junk bytes, and it refused as a `CratekitError`, was warned, and the guess went on. A bare error was not produced. `name apply` opens the same database the same way later in the same tail, so a pass already depended on this read before U172.

**Closes when:** a drive produces a bare database error on the read, or the read is wrapped the way `name apply`'s is if that one is wrapped first. Ledger only, reachability unmeasured.
