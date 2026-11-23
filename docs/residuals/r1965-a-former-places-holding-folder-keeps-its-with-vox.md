---
title: A row leaving a former place keeps the with vox and Favorites of the folder that holds the place
found: at the review of #1007, R-1965, round one, 2026-11-23.
issue: no
---

**The mechanism.** `adopt/move.py` `alongside_left` reads the places beside the band of the bucket being left, in that bucket's own folder. A former place (R-797) sits in another bucket's folder (NonElectronic), so a row `tag set` moves out of the declaring bucket leaves the former place but keeps the holding folder's `with vox` and Favorites.

**Measured cost.** Driven in review round one on a seeded row in NonElectronic / Soul / R&B with `with vox` and Favorites there, given Deep House by `tag set`, then `adopt move`: it ended in Deep House / High and still in NonElectronic / with vox and Favorites. The seeded state needs a filing made before the former place was declared, which was not driven.

**Closes when:** the holding folder's places beside the band are read for a row leaving a former place and left with it, Favorites under the same keep rule, with the seeded drive as its test.
