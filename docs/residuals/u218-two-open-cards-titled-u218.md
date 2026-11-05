---
title: Two open cards are both titled U218, #536 and #537, because parallel threads read the next unit number at the same time
found: at the build of #536, U218, 2026-11-05.
issue: no
---

**The mechanism.** The `file-card` skill takes a new card's number as one
past the highest U number any issue title carries. Two threads grooming the
board on 2026-11-05 read it within two minutes of each other: #536 was filed
at 14:14 and #537 at 14:16, both as U218. The same race gave two A93 cards
(#525, #528).

**Measured cost.** Read from the issue titles over REST. A unit number names a
record, `docs/restart/u218.md`, a mutation table and residual files, so the
later card's landing would write over or collide with the earlier one's
record, and the board names two units by one number. No library or DJ pays.

**Closes when:** the later card, #537, takes the next free number in its
title before it is built, and its record is named for that number. METHOD's
Sharing the board section, written by U218, now says a number is read just
before filing; a check in `board.py audit` that refuses two open cards with
one number would close the class. Ledger only: maintainer facing.
