---
title: The first sync of each pair after U202 lands reads its snapshot without the account's dates
found: at the review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** A snapshot recorded before U202 holds no account added
dates, and a track is read as put back on the account only against a date the
base recorded. So each pair's first whole sync after the landing applies
R-990's old rule once, and records the dates for the sync after.

**Measured cost.** Driven by the branch's own test of a snapshot without
dates: a track taken out and put back on the account in that one interval,
and taken out in rekordbox too, comes off the account. By design, said in
`modules/outbound/pairs.py`.

**Closes when:** every pair has had one whole sync since the landing. Ledger
only.
