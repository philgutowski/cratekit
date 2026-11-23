---
title: adopt move lists a row outside the library root as left with no reading, which is not why it stays
found: at the review of #1020, U956, 2026-11-23.
issue: no
---

**The mechanism.** Since U956 the census reads a row whose file resolves
outside `library.root` as `outside-root`, excluded, and never reads its energy.
`cratekit.adopt.move._standing_in_tree` gives every excluded entry held in two
competing subs the reason `no-reading` (`LEFT_NO_READING`), so `adopt move`
lists such a row as left for want of an energy reading though its file holds
one; a row outside the root held in a stale band is neither moved nor listed.
A `genre_moves` entry `tag set` recorded for it survives and is listed again at
the next gate. Leaving the row alone is what U956 asks; the reason shown is
what is wrong.

**Measured cost.** Driven by the round one reviewer only from a state built by
hand: a prefix rule mapping an outside folder onto itself, an `adopt apply` on
the base that filed the row (a rule from an old folder to a new one cannot,
since the base fails that pass), then `tag set` and `adopt move` on the branch.
The only outside rows measured on the real library, the 16 sampler rows, hold
no place, so the producer on a real library is unmeasured. `tag set`'s own
closing message was corrected in U956 and names such a row.

**Closes when:** `adopt move` names an outside row with its own reason, such as
`outside-root`, or leaves it out of its list, and a test drives a row held in
two subs outside the root. Ledger only: nothing is written wrongly and the
reachability on a real library is unmeasured.
