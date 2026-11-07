---
title: A continue of an order that moved nothing is held as reordered when the provider placed an added track anywhere but the end
found: at the build of #619, R-1420, 2026-11-07.
issue: no
---

**The mechanism.** The check reads the order of a part written pair whose
moves never began as the write leaves it (`_beyond` with `ordering` false in
`sync/pair_cli.py`): the plan's reading in its order, then this write's
additions after it. R-1411 found the provider may place an added track
elsewhere and lets it stand anywhere at the adapter; the check does not, so
such a continue refuses `decision-stale`, "was reordered since the plan".
The same rule held a continue stopped between its additions and its order
before R-1420; R-1420 applies it to every order that moved nothing.

**Measured cost.** Not driven against the provider: the shipped adapter
adds through the client's playlist add, which appends, and the discovery
suite's fake appends. Where it happens the cost is nothing written, a false
reorder named, and one more command, a fresh sync.

**Closes when:** the check reads the kept tracks' order and lets an added
track stand anywhere, as the adapter's agreed order does. Ledger only.
