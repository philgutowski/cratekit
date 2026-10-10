---
title: The ContentLink a native row is given is a vote over the library's history, not what rekordbox writes today
found: at the review of #292, U126, 2026-10-10.
issue: no
---

**The mechanism.** `row_link.library_link` counts every live row, however
old, and the landing gives its rows the value more than half of them carry.
On this library the old values are a minority, 2950670 on 10,312 of 10,498
live rows and on every row rekordbox made since 2026-03 but a few dozen, so
the vote and the recent rows agree. If a rekordbox update began writing
another value on new imports, the rows made before it would outvote the new
ones for as long as they are the majority, and every native row would carry
the older value. Whether rekordbox loads a row carrying an older value is
part of what is unknown about the column: the older values on this library
belong to rows that load, so the vote is the conservative reading today.

**Measured cost.** Not driven; no second value has appeared on recent rows.
A rekordbox version change is the trigger, and the pin check already stops
writes on an unvalidated version until someone validates it.

**Closes when:** what rekordbox derives ContentLink from is known, or the
validation of a new rekordbox version compares the value on its first own
import with the majority. Ledger only.
