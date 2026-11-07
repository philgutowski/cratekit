---
title: A Tidal move held as the order after a settled reading is put back when one sync in between reads the settled order again
found: at round two of the review of #623, U234, 2026-11-07.
issue: no
---

**The mechanism.** `_moved_since_stop` in `sync/pair_cli.py`: while an order
differing from the settled reading is held as the one after, a reading back
at the settled order (or on the moves' path) clears it and the stop is
finished from rekordbox's side. One such reading is trusted at once, though
the card rests on one reading after a stop being untrustworthy.

**Measured cost.** Round two's review drove it on the fixture (D2): the DJ's
move, held once as possibly theirs, was put back to rekordbox's order, the
gate naming the account as off the moves' path. On the real adapter R-1411's
agreed reading refuses the moves when the adapter's own read shows the DJ's
order, so the cost reaches Tidal only when that read lags too; not driven on
a provider. Holding the pair instead could hold it for good, which the
session judged the larger cost; `docs/GUIDE.md` says a reading in between
puts the move back.

**Closes when:** a sitting measures whether Tidal serves an older order again
after serving a newer one for the window. Ledger only.
