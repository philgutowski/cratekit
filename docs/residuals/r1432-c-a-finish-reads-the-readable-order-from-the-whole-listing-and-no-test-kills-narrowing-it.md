---
title: A finish reads the readable order from the whole listing with its unread ids, and no test kills narrowing it to the readable tracks
found: at the mutation table of #630, R-1432, 2026-11-07.
issue: no
---

**The mechanism.** `plan_pair` in `src/cratekit/sync/pair_cli.py` reads the
account at a finish of a stopped order as `pair_stopped.finished` leaves the
whole listing, unread ids included (U225 with R-1264), then keeps the
readable tracks. The adapter's rule keeps the longest tail of the asked
order already standing in order, so an unread track can change how long that
tail is, and with it which readable tracks the remaining moves put in front.

**Measured cost.** Row E4 of `docs/mutation/r1432.md`, `finished` read over
the readable listing alone, killed none of 17493 tests on the full suite.
Its composite, `docs/mutation/r1432-composites.md` row C4, the remaining
moves not applied at all, killed 35, so the finish read is pinned; whether
any listing makes the two readings of the readable order differ was not
driven, and the finished order of the asked tracks is the target's either
way, so a difference can only fall on a track added since the stop.

**Closes when:** a test finds a listing where the two readings differ and
pins the whole listing's, or the two are shown equal. Ledger only: an
existing guard sampled by this card, its reachability unmeasured.
