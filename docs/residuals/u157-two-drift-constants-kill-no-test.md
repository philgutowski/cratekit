---
title: Two of the drift measurement's constants kill no test
found: at the review of #338, U157, 2026-11-01.
issue: no
---

**The mechanism.** In `src/cratekit/analysis/detect.py` the onset gate's
relative fraction, `DRIFT_ONSET_RELATIVE`, can be set to 0.0 or 0.25 and the
window length, `DRIFT_WINDOW_SECONDS`, to 20, and `tests/test_analysis_drift.py`
stays green. The band, `DRIFT_BAND`, killed nothing at 0.06 or 0.5 before the
fix round; it is pinned on both sides since, by the stepped tracks below it and
the section of hats at three to two above it.

**Measured cost.** None of its own, driven by the review: the other gates
(the pulse contrast and the absolute onset floor) pass over the same synthetic
breakdowns. Whether a real breakdown passes the contrast gate and is held back
only by the relative one is unmeasured, since the container has no real audio.

**Closes when:** a fixture shows a window the relative gate alone holds back,
a loud riser over a breakdown for instance, and one shows a drift the window
length changes; or the attended calibration sitting finds the two do nothing
on real tracks and they are removed. Ledger only.
