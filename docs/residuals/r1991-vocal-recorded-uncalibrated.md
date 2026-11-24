---
title: A with vox playlist adopt apply recorded reads unexpected once the library has no vocal calibration
found: at the review of #1022, R-1991, 2026-11-23.
issue: no
---

**The mechanism.** `adopt apply` now records its vocal additions' playlists.
A recorded destination is compared on every check whatever this run derived,
and the check's own filter takes only the playlist signal dimension out of
`unexpected`, so with no calibration the recorded `with vox` playlist's tracks
read `unexpected`. A rebuild's record has the same shape for a vocal
destination it recorded while calibrated.

**Measured cost.** Driven at round one at the check: with a threshold the
tree converges, without one `unexpected:deep_house/with_vox:1`, where the
base said matching. Losing the calibration after an adoption filed a vocal
membership was not driven through a verb.

**Closes when:** the check leaves a recorded destination in a dimension this
run did not compare out of `unexpected`, as `left_behind` already does.
Ledger only, the reachability unmeasured.
