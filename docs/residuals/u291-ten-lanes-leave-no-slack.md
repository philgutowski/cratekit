---
title: Ten lanes against a cap of ten threads leave no slack, so a hold board.py cloud counts and the coordinator does not stops the thread it starts next
found: at the review of #848, U291, 2026-11-21.
issue: no
---

**The mechanism.** Until U291 `CLOUD_LANES` was five against the building
project's cap of four threads, and METHOD said the coordinator "leaves the
fifth lane empty". That spare lane absorbed any hold `board.py cloud` counts
while the coordinator does not: a session that died under eight hours ago,
whose `Started` is still read as `underway`, or a freshly relayed answer read
as a hold (R-1666). Phillip's decision of 2026-11-21 sets both to ten, so with
ten threads running and one such hold the queue prints `Held, 10 of 10` and
`Every lane is held`, and the cloud-unit skill's Orient step tells the thread
the coordinator just assigned to stop; if that thread has already posted
`Started`, the reader exits 1 with `MORE CARDS ARE HELD THAN THERE ARE LANES
(11 for 10)` and tells it to post `Withdrawn`. R-1280 and R-1666 both rested
their "nobody pays" on the old five against four.

**Measured cost.** Driven by the reviewer on a scratch copy with the test
file's doubles: ten live holds, one hold an hour old whose session is gone,
and the next assigned card. The old setting printed `Held, 4 of 5` and
offered the card; the new one offers nothing. The cost is a lane idle until
the stale hold passes eight hours, or until the coordinator's next hourly
fill, per dead thread. Maintainer facing; no user of a shipped verb pays.

**Closes when:** the cloud-unit skill says a card the coordinator assigned is
built whatever the lane alarm says (R-1666's own condition), or the reader
stops counting a hold the coordinator does not, with a test. Ledger only.
