---
title: The steps unread note says anything an earlier command wrote refuses stale, which an account order's blind moves never did
found: at the review of #595, U231, 2026-11-07.
issue: no
---

**The mechanism.** `sync_pair`'s `sync-pair-steps-unread` note says that
with the run's steps unreadable "anything an earlier command of run N wrote
refuses stale rather than being written twice". Round two's review drove a
continue whose steps were unreadable or gone sending an order's moves a
second time, the check passing because the provider still served the order
from before them. The second fix round closed the resend by reading the
carried record (`PairSteps.carried`); the note's sentence is still stronger
than what holds for the rest of a pair's write.

**Measured cost.** None left for the order after the fix; a wording that
overclaims.

**Closes when:** the note says the carried record is read for an order and
names what else refuses stale. Ledger only.
