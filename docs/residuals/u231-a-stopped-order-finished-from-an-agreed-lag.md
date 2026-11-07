---
title: An order stopped part way whose two readings agree on a lag longer than five minutes has its remaining moves sent by position from that lag
found: at the review of #595, U231, 2026-11-07.
issue: yes
---

**The mechanism.** A write stopped part way through its order (no `moved`
step) is pending; once two readings at least `AGREE_AFTER` (five minutes)
apart agree on an order on the moves' path, `_pending` in
`sync/pair_cli.py` lets the plan finish it from the leading side, as U225
finishes a stopped write and as the brief asks. If the provider serves the
same stale order for longer than five minutes, the agreed reading is that
lag, and the remaining moves are planned from it and sent by position, one
of them already sent, which scrambles the account playlist.

**Measured cost.** Driven by round one's review on the fakes (T7, the verb)
and on the order suite's provider (T9, the adapter): the second order write
went out from the served old order and left d, c, b, a for an asked d, c, a,
b. Whether the live provider's lag after a stopped write outlasts five
minutes and agrees with itself was not driven; Sitting 86 measured orders
not served after 28 minutes, but reads 3 s apart then disagreed.

**Closes when:** a stopped write is finished only from a reading that also
agrees with where the recorded moves could have left it after a longer wait,
or the attended proof (A88, A91) measures the lag and the window is sized to
it. Earns an issue: an account playlist can be damaged.
