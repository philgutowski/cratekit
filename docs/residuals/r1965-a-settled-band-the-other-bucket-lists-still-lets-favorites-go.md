---
title: A band the new genre's bucket settles but lists rather than moves still lets the old folder's with vox and Favorites go
found: at the review of #1007, R-1965, round two, 2026-11-23.
issue: no
---

**The mechanism.** `adopt/move.py` `leaving_moved` counts a place settled in the other bucket (`settled_in_the_other_bucket`) as left for the Favorites rule, on the ground that the bucket the entry claims takes it out in the same job. Where that bucket's `standing` lists the track instead (no reading, or the band held under another name only), the move out of the old folder still removes its `with vox` and Favorites while the track stays in the old folder's band.

**Measured cost.** Driven in review round two on a seeded state: an R&B row with no energy tag in R&B High, with vox, Favorites and Soul Low, given Soul by `tag set`, then `adopt apply` and `adopt move`. It ended in R&B High, Soul Low and Soul Unsorted with the entry spent; `favorites refresh` then planned putting R&B's Favorites back. The seeded mix of an R&B band and a Soul band was not produced by a verb.

**Closes when:** a settled place counts as left only when the claiming bucket's standing is a move removing it, asked through the same plan pass, with the seeded drive as its test.
