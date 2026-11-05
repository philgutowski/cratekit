---
title: A sync pair stopped on an unfinished order reports no totals of what it wrote
found: at round one's review of #543, U220, 2026-11-05.
issue: no
---

**The mechanism.** When an account order does not finish, `sync_pair` writes
every other pair and then raises one refusal, whose envelope carries the
refusal's detail (the unordered pairs, the run, how many finished) and not
the totals a finished sync reports (tracks added and taken off each side,
playlists made, jobs queued). The continue's totals count only its own
command's writes.

**Measured cost.** An under report, not a false one: driven through the verb,
another pair's added track and a playlist brought into rekordbox appear in
neither envelope.

**Closes when:** the stop's detail carries the totals of the writes it made.
Ledger only.
