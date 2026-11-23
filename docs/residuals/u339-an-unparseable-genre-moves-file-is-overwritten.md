---
title: An unparseable genre_moves.json reads as no entry, and the next tag set overwrites it
found: at the review of #988, U339, round one, 2026-11-23.
issue: no
---

**The mechanism.** `adopt/genre_moves.py` `read` answers no entry for a file it cannot parse, on purpose, so a damaged file never removes a membership. `record` then writes the merged entries over it, so the entries it held are gone and `adopt move` never plans those rows' moves out of their old genre folders.

**Measured cost.** Driven with the file corrupted by hand after one run: the next `tag set` rewrote it and the earlier rows were not moved. Nothing in the product writes the file other than atomically, so the producer is a hand edit or a disk fault; the cost is a track left in its old folder as well, as before U339, and visible in rekordbox.

**Closes when:** `record` refuses, or keeps the unreadable file beside under a dated name, when the file exists and does not parse, with a corrupted file as its test.
