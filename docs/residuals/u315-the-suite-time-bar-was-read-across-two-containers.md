---
title: The suite's time bar was read against an absolute number measured on another container, so U312's met is not reproduced like for like
found: at the build of #872, U315, 2026-11-23.
issue: no
---

**The mechanism.** Point 5 of U290 asks the suite to run at least 30 percent faster on the cloud runner, and the survey turned that into 351 seconds, 70 percent of the 501.69 it measured at `ff8e5ec` on its container. #869 (U312) timed its branch at a 314.95 second median on its own container and called the bar met, but did not time `ff8e5ec` there. U315 timed both on one four core container: `main` at `d289f61` 425.13, 408.64 and 399.36 seconds (median 408.64), `ff8e5ec` from its own clone and venv 554.96, 479.45 and 489.08 (median 489.08). So `main` is 16.4 percent faster, not 30, on a container whose `ff8e5ec` reading is within 3 percent of the survey's. Containers differ by more than the margin the bar leaves.

**Measured cost.** Maintainer facing: a time bar read as met was not. No verb is affected.

**Closes when:** #985 (U336) meets the bar with both commits timed on one container, and METHOD or the cloud-unit skill says a timing bar is a ratio measured base and branch on the same container. Ledger only.
