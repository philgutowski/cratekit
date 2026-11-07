---
title: A move the provider answers false or not found is read as one whose landing is not known
found: at the build of #604, R-1394, 2026-11-07.
issue: no
---

**The mechanism.** `order_tracks` in `modules/outbound/tidal_account.py`
brings the record's `sent` count back down only for a move whose last answer
was a 412, the one answer Sitting 62 measured as changing nothing. A move
the client answers `False` (a response that was not ok) or not found is
raised as "the provider did not accept the move" with `sent` left counting
it, so a stopped order whose last move was refused that way holds an agreed
reading at the moves before it, as for a dropped connection (the residual
beside this one), although that move most likely changed nothing.

**Measured cost.** Not driven against the live provider; what a not ok
answer to a move leaves on the playlist was not measured. The cost is a pair
held that could have finished, never a scramble.

**Closes when:** an attended sitting reads a playlist after a move the
provider answered not ok, and the answer is added to the ones that bring
`sent` down if it changed nothing. Ledger only.
