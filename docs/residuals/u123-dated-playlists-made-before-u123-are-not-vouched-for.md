---
title: A dated playlist U117 made before U123 landed is not vouched for, so label heard refuses to remove it
found: at the review of #282, U123, 2026-10-10.
issue: no
---

**The mechanism.** `label heard` takes tracks off or removes a dated playlist
only when the outbound ledger records it as made here, and the ledger learned to
record one in this unit, through `reserve_label_dated`. A dated playlist
`crate organize` created between U117 landing and this unit landing has no such
record, and the dated plan reuses it by name without ever recording it, so the
verb refuses it before the gate with `label-heard-not-product-made`. A plan
that only marks releases heard, KEEP or ABSENT, is not refused.

**Measured cost.** Not driven against the live account. The window is the time
between the two landings, and the remedy is in the refusal: merge and remove
the playlist by hand, then run the verb again to mark its releases heard.
Recording such a playlist as made here after the fact would take the product's
word for a playlist nobody can prove it created, which is the one judgement the
ledger exists not to make.

**Closes when:** every such playlist has been merged by hand once, or the author
decides to vouch for them by a recorded, attended act. Ledger only.
