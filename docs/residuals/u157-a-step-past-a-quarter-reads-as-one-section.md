---
title: A tempo step of more than a quarter reads as the section the head named
found: at the review of #338, U157, 2026-11-01.
issue: no
---

**The mechanism.** Each drift window's peak is looked for within a quarter of
the head tempo either way (`DRIFT_BAND`), so a window cannot read a related
metrical level, four to three, three to two or two to one, as a drift. A track
whose tempo really steps by more than that, 100 to 140 for instance, has its
other section's windows passed over, and reads as steady.

**Measured cost.** Driven by the review: a synthetic 100 to 140 step read 0.05
and steady. How often a real track steps by more than a quarter is unmeasured;
a step that large is also where a pulse at a related level and a new tempo
cannot be told apart from the onsets alone.

**Closes when:** a measurement that tells a real step from a level change, the
key or the spectrum changing with it for instance, reads such a track as
variable without reading the hats of a steady track as one; or the attended
calibration sitting finds no such track in the library. Ledger only.
