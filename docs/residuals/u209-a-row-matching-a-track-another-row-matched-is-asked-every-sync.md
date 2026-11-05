---
title: A rekordbox row whose ISRC matches a track another row of the playlist already holds is asked about on every sync
found: while recording U209's no change cost, #499, 2026-11-05.
issue: no
---

**The mechanism.** `plan_pair` asks the account about an unlinked row
(`_ask`) before it checks whether the track the answer names is already the
match of another row of the same playlist (`seen_remote`). The second row is
then named unmatched with "another row of this playlist ... is already the
account track it matches", is neither linked nor remembered as a miss, and the
next plan asks again. A row whose answer named an unreadable candidate is
likewise never remembered, by R-988's own rule.

**Measured cost.** Read from the code, not driven live. One lookup per such
row per sync; since U209 a sync plans once, so it is one per sync rather than
three. How many such rows Sitting 54's library holds is unmeasured.

**Closes when:** a row matching a track another row holds is checked against
the held remote ids before the account is asked, or remembered with that
reason until either row changes. Ledger only.
