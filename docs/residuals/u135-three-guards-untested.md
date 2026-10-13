---
title: three of U135's guards have no test that reaches them, the mutation table measured them at zero
found: by the watcher's measurement of the u135 table on main ae06140, 2026-10-13.
issue: yes
---

**The mechanism.** `docs/mutation/u135.md` rows A6, A11 and A15 survived the full suite:
`recorded_inbox_playlist` accepting a soft deleted row, the apply time re check of a removed
batch playlist in `_batch_playlist_row`, and a folder carrying the set's name being taken as the
INBOX playlist. Each guard is right by reading, and the independent review drove the sibling
guard that A1 covers, but nothing in `tests/test_u135_set_inbox_join.py` reaches these three.

**Measured cost.** None to a person today. A regression in any of the three would file tracks
into a deleted or folder row without a test turning red.

**Closes when:** three driven tests, one per row, kill A6, A11 and A15 on a rerun of the table.
