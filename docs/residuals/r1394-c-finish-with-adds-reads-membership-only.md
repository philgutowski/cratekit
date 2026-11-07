---
title: A write that finishes a stopped order and also adds or removes tracks still plans its moves from a reading checked by membership alone
found: at the review of #604, R-1394, 2026-11-07.
issue: yes
---

**The mechanism.** Round one's review drove the second half of R-1394's
measured cost: the plan finishes a stopped write only from an agreed reading
at or past the moves sent, but the write that follows plans its remaining
moves from the adapter's own fresh reading, which `_settled` in
`modules/outbound/tidal_account.py` accepts on the tracks it holds, not
their order. Its fix round passes the check's listing as `expect` (compared
in order) when a write finishes a stopped order, in `_write_account` in
`sync/pair_cli.py`. Where that same write also adds or removes tracks on the
account, the listing is no longer the playlist and the old membership check
stands, so a reading that lags the stopped order's moves seconds after a
true one still has the moves sent by position from it.

**Measured cost.** Round one drove the adapter half on the order suite's
provider: one move in, the next read lagging it, `order_tracks` left d, c,
a, b for an asked d, c, b, a and reported it done. The case with additions
or removals alongside was not driven, and whether the live provider lags a
read seconds after serving the truth was measured at Sitting 86 (reads 3 s
apart disagreed), not here.

**Closes when:** the adapter takes an agreed order beside its membership
check, every track of the agreed reading it still holds standing in that
order, and the finishing write passes it whatever else it writes. Earns an
issue: an account playlist can be damaged.
