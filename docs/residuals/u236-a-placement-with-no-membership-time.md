---
title: A favourite's month placement whose membership time is not read at the write is not recorded, and its unfavourite is again beaten by the library's own month
found: at the review of #628, U236, 2026-11-07.
issue: no
---

**The mechanism.** `organize/mirror_edits.write` reads the time of the
membership each FAVOURITE's month placement made
(`account_mirror.membership_times`) after `assert_read_back`, and `settle`
records the placement after `write` returns. Both run only on the happy path.
A database that refuses that read gives no time, and the placement is skipped
with nothing said. A read back refusal after the commit (`session-committed-unverified`)
leaves the month written and nothing settled or placed. Either way the next
refresh reads the library's own month as an addition made in rekordbox, sitting
88's shape, for that one track.

**Measured cost.** Fable's round two drove the cost by forcing the time read
empty during the carry: the unfavourite was listed "placed in the favourites in
rekordbox since: an addition beats a removal" and the track stayed a favourite.
The direction is conservative, a favourite kept, never one removed. No real
producer was driven: `rb_writer` writes `created_at` on every membership, and
the read back has just read the row.

**Closes when:** the step warns when a FAVOURITE's month placement has no time,
or the placement is recorded from the plan's own month and the read back's
rows, and a test drives each. Ledger only.
