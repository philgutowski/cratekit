---
title: The night pass's second fix round was not reviewed
found: at the landing of #850, U293, 2026-11-21.
issue: no
---

**The mechanism.** METHOD caps a unit at two fix rounds, and U293 spent both: round one fixed the night's record as a snapshot, round two found that `settle` ended a wait on an answered gate or an empty folder, and the second fix (`04508be6`) made a wait end only on the pass's own native landing, read through `intake.native.landings_of_pass`. No third review read it.

**Measured cost.** None measured. The fix is pinned by tests for an answered gate over staged tracks, a landed pass with another pass's file staged since, an emptied folder and an unreadable landing log, and by mutation rows N6 and N7. What a review would look at: a pass that is aborted and whose tracks are then left staged keeps the night refusing on the folder until they are landed or moved, which is the conservative reading; and `landings_of_pass` reading a library on the bridge rather than native, where no native landing is ever recorded and a wait would never settle by itself (the next firing that runs still writes a fresh record).

**Closes when:** a review of `04508be6` against the night's record, or the attended night card reads one real night's record through a landing.
