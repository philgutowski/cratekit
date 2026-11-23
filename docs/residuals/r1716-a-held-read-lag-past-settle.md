---
title: A held sync removed read trusts the provider to serve a playlist's current tracks half an hour after its stamp moves, and a change that keeps the count past that is held for six hours
found: at the review of #1010, R-1716, round two, 2026-11-23.
issue: no
---

**The mechanism.** `sync/removed_kept.py` holds a synced playlist's read
only when it holds as many tracks as the account's listing counts and the
listing's last updated stamp is at least `SETTLED` (30 minutes) older than
the read, and reuses it for `HELD_FOR` (6 hours) while the listing shows the
same count and stamp. A change that keeps the count (a swap of one track for
another) whose old tracks the provider still serves more than 30 minutes
after the stamp moved is read old, held, and answers every run for six
hours. Round two drove it on a stand in: the listing current, the rows old,
the stamp 31 minutes back; New1, swapped onto another synced playlist, was
offered for removal from the collection until the hold ended, where a fresh
read keeps it.

**Measured cost.** Not driven against the provider. The one measured lag is
sitting 86's, a paged read serving a playlist's old order for at least 13
minutes after a move (`docs/cutover.md`); a removal showed none at sitting
101. A lag on a swap or an add, or one past 30 minutes, has not been
measured, nor the spelling of `lastUpdated` the live listing sends (with no
zone it marks nothing and nothing is ever held, which costs calls only).

**Closes when:** an attended sitting measures how long the provider serves a
playlist's old tracks after a swap and an add, and what `lastUpdated` the
account listing sends, and `SETTLED` is set from that; or the read compares
the opened playlist's own count and stamp with the listing's before it is
held. Ledger only: the input was not produced, and the attended card filed
with #1010 measures it.
