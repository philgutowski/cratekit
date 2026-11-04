---
title: A matched row of a new pair is asked of the provider once per plan, three times per sync
found: at the review of #483, U198, 2026-11-04.
issue: no
---

**The mechanism.** U198 remembers a row the account has no track for before the gate (R-988), but a row it does match is linked only when the pair is written. One sync plans three times, once per invocation the two explicit gates make, so every matched row of a new pair is asked three times on its first sync.

**Measured cost.** Driven by the review on the fake account: a first sync of a four row playlist made twelve `match_track` calls. Over the roughly 112 playlists outside ARCHIVE the first live run asks about three times each row, paced by the provider gate. Not measured live; the attended card records the run's request count.

**Closes when:** the links a plan made are carried through the run, as the misses are, so the gates' plans reuse them. Ledger only.
