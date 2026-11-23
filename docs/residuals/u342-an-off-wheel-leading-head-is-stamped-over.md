---
title: A title that is or holds a head the parser does not read as leading, 13A - 124 - Alpha, 06A - 124 alone, or one behind the marker, is stamped as a title with no head and carries two
found: at review round one of #994, U342, 2026-11-23.
issue: no
---

**The mechanism.** `core/naming.py`, `stamp_head`: the head parser reads a key
only on the wheel, 1A to 12B, so `13A - 124 - Alpha` has no head to it and
is given one, `06A - 124 - 13A - 124 - Alpha`. A title that is a head and
nothing else, `06A - 124`, has no terminator after its tempo, so it is no head
either and becomes `06A - 124 - 06A - 124`; a head behind the lossy marker,
`[MP3] 8A - 125 - Alpha`, becomes `06A - 124 - [MP3] 8A - 125 - Alpha`. A
head at the end of a title is refused since review round one
(`strip_trailing_head`), these are not.

**Measured cost.** Driven at review round two through the landing and the
verb: a title tag `13A - 124 - Alpha` lands unchanged and adopt writes
`06A - 124 - 13A - 124 - Alpha` to the row, the tag and the key tag; `06A -
124` lands and is written `06A - 124 - 06A - 124`, and a second run agrees.
Every byte is kept and the session record restores it. The marker case was
driven on the pure function; the landing turns that tag into `08A - 125 -
[MP3] Alpha`, which is then left. No producer of any of these tags upstream
of staging was driven: every writer of a head renders through the same
engine.

**Closes when:** a producer is found, then `stamp_head` refuses a title that
begins, after any marker, with a shape of key and tempo whatever the key's
number or what follows. Ledger only.
