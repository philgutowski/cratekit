---
title: A split pair whose second genre cannot be read is planned out of its R&B band, and the gate says nothing
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** Adoption's census reads a file's second genre through
`adopt/scan.py`'s `_second_of`, which answers an unreadable tag as no second
genre. A Soul track whose second genre is R&B then has one entry, Soul's, and
R&B's band reads as Soul's split place again, which `adopt move` plans to take
it out of. Nothing on the gate says the second genre went unread.

**Measured cost.** Driven at round two with `read_second_genre` made to raise
`TagReadFailed`: the gate planned Soul's move removing `rnb_med`, with no
warning. Whether a file whose energy reads can fail on its second genre was
not measured; both come from one container.

**Closes when:** a census that could not read a second genre leaves that
track's R&B band alone, or names the file on the gate. Ledger only.
