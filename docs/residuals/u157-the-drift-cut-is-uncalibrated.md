---
title: The drift cut ships at 1.5 without a reading of any real library
found: at the build of #338, U157, 2026-11-01.
issue: no
---

**The mechanism.** `analysis.drift_cut` defaults to 1.5 percent
(`core.config.DEFAULT_DRIFT_CUT`), chosen from synthetic tracks: steady drum
patterns read 0.0 to 0.3, a played part's timing wobble around a fixed tempo
0.3, a wander of two beats either way 1.5, a three beat ramp over two minutes
1.7, a step of 120 to 140 above 17. The brief asked for the cut to be
calibrated against the 2026-10-27 batch, which holds both kinds, and the cloud
cannot read it.

**Measured cost.** Unmeasured on real audio. A cut too low sends steady tracks
to Dynamic, which the brief's evidence shows lays a wobbling grid; a cut too
high sends live tracks to Normal, which is what every track took before this
unit. The default leans toward the second.

**Closes when:** an attended sitting runs `crate analyze run` over copies of a
batch holding both kinds, reads each file's `driftlevel`, and sets the default
from where the two kinds part, recorded in `docs/cutover.md`. The attended card
this unit files is that sitting. Ledger only.
