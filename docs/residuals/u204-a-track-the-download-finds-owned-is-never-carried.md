---
title: A track added on the account that the download job finds owned by a rule mirror-downloads cannot see is queued, then named and never carried
found: at the review of #494, U204, 2026-11-05.
issue: no
---

**The mechanism.** `mirror_downloads._owned` reads the database's ISRC column
and the mirror matcher's codes. The `intake playlist` job owns a track by
`intake_cli.resolve_track`'s rules over the files: ISRC_EXACT, EXACT artist and
title and version, CREDITED_EXACT. A row whose code is only in its file and that
sits in no mirrored playlist, one with no code at all, or the same artist and
title under another code, is missed by the step, so the track is queued; the job
resolves it owned and lands nothing. Since round two the step names it as
found owned rather than awaiting a landing, but the account's edit is never
carried, since no library row is tied to the account track.

**Measured cost.** Driven by review round two through the real handler (three
populations): one queued job and one request per such track, the edit named
on every run and never taken. The file only population is unmeasured; the
untagged one is the matcher's count, 1691 of 9868 live files with no ISRC tag,
measured on the tree by an earlier unit.

**Closes when:** the step asks the job's own rule (`match_cli.library_view`
with `resolve_one`) before queueing, and ties an owned answer to its row so the
edit is carried. Ledger only: the product says what happened.
