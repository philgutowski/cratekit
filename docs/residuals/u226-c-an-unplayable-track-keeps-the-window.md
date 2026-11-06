---
title: A playlist holding a track the account cannot play never has a whole unpaged read, so its window is judged as before U226
found: at round one of U226's review (#578), 2026-11-06.
issue: no
---

**The mechanism.** `acquire.listing.judge_window` takes the unpaged read as
the playlist only when it holds the declared count, which keeps the declared
total rule. A track the account cannot play is left out of both reads and
still counted, so for such a playlist neither read is ever whole: a window
that lags is a lag (the pair held, the read back refused after its pauses)
and an order or removal is refused `positions-unknown`, as on main.

**Measured cost.** Read at round one, not driven live: whether a paired
playlist on the account carries such a track was not measured. No new cost
against main, which refused the same writes; the pair is held for the lag's
length rather than planned from a stale window.

**Closes when:** a reading can place the unplayable track (the items
endpoint, which counts it), if a sitting finds a paired playlist carrying
one. Ledger only.
