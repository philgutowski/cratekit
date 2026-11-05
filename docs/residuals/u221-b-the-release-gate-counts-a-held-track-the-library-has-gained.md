---
title: The release gate counts a held track the library has since gained, so it can name more than the next sync pair queues
found: at the review of #549, U221, 2026-11-05.
issue: no
---

**The mechanism.** `crate sync release` (`sync/release_cli.plan`) counts every
id a twin's recorded hold carries. Once the library gains one of them, by a
hand import, `crate sync pair` links it and adds it to the twin, but the
pairs document still holds its id, so the release gate names and counts it.
Fix round one subtracted the pair's recorded links; round two found that read
raw links the document never prunes, so a link whose row left the library hid
a held track and could make a twin unreleasable, and fix round two put back
the count of every recorded id.

**Measured cost.** Driven on the twins world by round one of U221's review:
three held, a row carrying one track's ISRC inserted, `sync pair` added it to
the twin; the release gate said "3 track(s)" and the next `sync pair` queued
two. A count on the release screen one or more above what the sync pair gate
then shows and queues; nothing is downloaded, lost or blocked by it.

**Closes when:** the release plan subtracts only a held id whose link names a
live library row, read as `sync pair` reads it, or `sync pair` drops from the
recorded hold an id it has linked. Ledger only: a count the next gate corrects.
