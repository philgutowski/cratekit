---
title: An unread track that the account reads after a stop and the person then moves still lets the account lead, as any readable move does
found: at the review of #639, R-1446, round one, 2026-11-08.
issue: no
---

**The mechanism.** `_readable_moved` in `src/cratekit/sync/pair_cli.py`
leaves out only the ids the account lists unreadably now. A track unread at
the stop, read settled while unread, and readable once Tidal fills in its
title is a readable track to U234's settled comparison, so a move of it after
that is read as the person's reorder and the account leads, its readable
tracks in the stopped write's half done order.

**Measured cost.** Driven by the review (round one, P8): rekordbox goes to 1,
2, 3, 9, 4, the same on main. It is U234's rule that a settled move of a
readable track leads, applied to a track that was unread when the stop was
read. How often Tidal fills in a title after the fact is not measured.

**Closes when:** a track read unread at the stop is read by its place at the
stop rather than as readable since, or the case is decided to be the person's
reorder and recorded so. Ledger only: U234's own rule on a track whose
reading changed.
