---
title: A bucket the upgrade adds takes its exact words from the copy's keyword rules without a hold
found: at the review of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** The upgrade's collision check compares the words buckets and
their subs declare. It does not read the copy's `[[fuzzy]]` keyword rules or
its vocabulary, so a copy that routes the exact genre "Soul" through a keyword
rule to another bucket gains a Soul bucket whose exact alias wins over the rule,
with no hold. That is the routing the shipped template itself has (an exact
alias before a partial keyword), and the gate lists the bucket by id, so the
person approves the bucket; what the gate does not say is which of their
keyword routed words change folder. Not driven against such a copy.

**Measured cost.** Tracks of exactly that genre file into the new folder on the
next adoption or rebuild instead of the one the keyword rule chose. Nothing is
lost, and adopt move or a rebuild moves them again if the bucket is taken out.

**Closes when:** the plan names, per added bucket, the copy's keyword rules and
vocabulary rows its words take over, or holds on them. Ledger only.
