---
title: The light worker's declared cost was measured on one Linux container, and three of librosa's own transients now set it
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** `analysis/light.py` declares a light worker at 320 MB plus
1.5 MB for each second of the batch's longest track, from peaks measured in a
fresh process per track on the container U241 was built in: 238 MB at two
seconds, 345 at 45, 564 at 240, 860 at 445, 1092 at 600, 1175 at 660. After
the separation's blocks the peak is no longer one stage's: for the eleven
minute track the decode reached 567 MB, the tempogram 820, the separation
1064 and the constant Q transform 1175, each a transient of about 650 to 780
MB over a floor that rises as librosa's kernels compile. The decode, the
tempogram and the transform are librosa's and are not blocked here.

**Measured cost.** None observed: the declared figure is above every measured
one. Unmeasured: the same peaks on macOS on Apple silicon, where the
allocator, the BLAS and librosa's build differ. A cost that read low there
would let the planner afford a worker the machine cannot carry, which the
headroom, the reserve and the pressure gates stand behind.

**Closes when:** `scripts/analyze_stages.py memory` is run on the Mac over
library tracks of mixed length and the two constants are confirmed or
replaced from its table, which U241's attended card asks for. Lowering the
peak further means computing the tempogram and the transform in blocks, which
touches tempo and is its own unit. Ledger only.
