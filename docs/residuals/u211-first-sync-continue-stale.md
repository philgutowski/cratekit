---
title: A first sync of a pair refused at its write is continued stale, because approving marked the pair and the digest covers the mark
found: at the build of #505, U211, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_cli.apply_pair` marks a pair in the pairs
document before it writes either side, and `PairPlan.identity` puts `marked`
in the digest both gates bind to. So when a pair's first sync, or a pair the
sync makes, is refused at its rekordbox write (by U211's unconfirmed absence,
or by any refusal there), the run U211 keeps is continued with `--run` into a
plan whose digest moved, and each gate refuses `DECISION_STALE` in turn and is
answered again, both of them. A pair already marked, which is every pair in a sync of every
pair and the case Sitting 54 met, digests the same and continues straight
through, as `tests/test_process_scan.py` drives.

**Measured cost.** Driven on the disposable library while building U211: the
continued run of a new pair's first sync answered `DECISION_STALE`. The round
one review drove it to the end: stale on `sync.pair.rekordbox`, answered,
stale on `sync.pair.account`, answered, then written with nothing lost. That
`marked` is the field that moved is read from the identity, not isolated. Nothing is written under a stale answer, so the
cost is both gates answered again and two more plans, each of which asks
the provider again.

**Closes when:** a refused first sync continues without asking again, by
marking the pair only once a side is written, or by leaving `marked` out of
the digest of a pair the same run marked. Ledger only: nothing is lost or
misreported, and the workflow finishes.
