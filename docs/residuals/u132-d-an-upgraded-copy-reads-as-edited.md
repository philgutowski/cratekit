---
title: An upgraded taxonomy copy reads as edited, so doctor stops saying when it falls behind again
found: at the review of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** `crate taxonomy upgrade` rewrites the active copy and leaves
the origin record setup wrote (R-689) as it was. Doctor's `_origin_verdict`
compares the copy's digest with the record's, so after an upgrade it answers
"edited since setup copied the shipped template", and a later shipped change
inside a section both declare (a fuzzy rule, a vocabulary row) no longer raises
the "fell behind" INFO. Read from the code, not driven.

**Measured cost.** The sentence is true, the copy was edited, by the upgrade on
the person's answer. What is lost is the R-689 notice for changes inside
existing sections; the new `taxonomy.schema` check still names any class or
bucket the copy lacks, which it never did before this unit. The live library
has no origin record at all, so it loses nothing.

**Closes when:** the record can say which shipped text a copy was last brought
up to, read by doctor, or a decision records that an upgraded copy is the
person's. Ledger only.
