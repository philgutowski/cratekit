---
title: A title led by a head whose key is off the Camelot wheel, 13A - 124 - Alpha, is stamped as a title with no head and carries two
found: at review round one of #994, U342, 2026-11-23.
issue: no
---

**The mechanism.** `core/naming.py`, `stamp_head`: the head parser reads a key
only on the wheel, 1A to 12B, so `13A - 124 - Alpha` has no head to it and
is given one, `06A - 124 - 13A - 124 - Alpha`. A head at the end of a title
is refused since the review (`strip_trailing_head`), a malformed one at the
front is not.

**Measured cost.** Driven on the pure function only. No producer of an off
wheel key in a title was driven: every writer of a head renders through the
same engine, which refuses a key off the wheel.

**Closes when:** a producer is found, then `stamp_head` refuses a leading
shape of key and tempo whatever the key's number. Ledger only.
