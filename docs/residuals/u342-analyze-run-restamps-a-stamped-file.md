---
title: analyze run pointed at a file analyze adopt stamped measures and names it again, putting its own key over rekordbox's
found: while building #994, U342, 2026-11-23.
issue: no
---

**The mechanism.** `analyze adopt` gives a title with no head one built from
rekordbox's key and tempo, in the row's title, the title tag and
`initialkey`, and never renames the file, so the file name keeps having no
head. `analyze run`'s resume marker (`analysis/run.py`, `already_analyzed`,
and `analysis/cli.py`, `carries_head`) reads the head off the file name only,
so the stamped file reads as never analysed.

**Measured cost.** Driven on the workers suite's fixtures with a fixed
detector: a file `Sierra.flac` whose title tag is `06A - 124 - Sierra` and
`initialkey` `06A`, put through `crate analyze run` over its folder, came out
as `08A - 124 - Sierra.flac`, title tag `08A - 124 - Sierra`, `initialkey`
`08A`: rekordbox's key replaced by Cratekit's, and the file renamed. A file
in the collection renamed by `analyze run` is a separate, older exposure of
any headless library file. The producer is a person pointing `analyze run` at
a library folder after the visit; today's landings carry a head from
`analyze run` before they land, so a stamped file is rare until U343, and the
reachability on a real library was not measured.

**Closes when:** U343 (#995) lands, which removes the key stage, the head,
the `initialkey` write and the rename from `analyze run` and resumes it by a
tag the run writes. Ledger only: the card that closes it is already queued.
