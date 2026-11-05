---
title: A batch with no record and no creation date is said to have no landing record while a session record could not be read
found: at round two of the review of #512, U214, 2026-11-05.
issue: no
---

**The mechanism.** `rotate._classify` names a recognised batch with nothing to
age it from "no landing record and no creation date to age it from", without
the unread clause U214 gave the unrecognised reason. The gate's
`rotate-records-unreadable` warning still fires beside it.

**Measured cost.** A reason that overclaims, with a true warning beside it.
Driven with the playlist's creation column set empty in SQL; rekordbox always
fills it, so the producer is synthetic (1 candidate driven).

**Closes when:** the reason carries `Landings.unread()` as the unrecognised one
does. Ledger only.
