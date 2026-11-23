---
title: A Soul row still in an R&B band, given a third genre by tag set, is recorded as leaving Soul and the move neither moves nor lists it
found: at the review of #1007, R-1965, round two, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/genre_set.py` `_leaves` records the bucket the row's old genre names (Soul), while the row sits in the bucket that holds Soul's split place (R&B). `adopt move` asks Soul for that row, which holds nothing there, so it plans nothing and lists nothing, and the row stays in R&B beside its new folder. The path is U339's, untouched by R-1965.

**Measured cost.** Driven in review round two on a seeded state (a Soul row in R&B High, with vox and Favorites, given Deep House): the answer said the move takes 1 row out, the plan was empty, and the row stayed in R&B with the entry recorded for Soul. The one verb chain tried does not produce the state; `tag retag` and `tag remap` were not driven. Not measured on main.

**Closes when:** `_leaves` records the bucket the tree actually holds the row in (the split place's holder too), with the seeded drive as its test.
