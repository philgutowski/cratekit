---
title: The vocal worker's declared gibibyte is under its measured peak on a long track
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** `VOCAL_WORKER_BYTES` is one gibibyte, the source system's
budget. U241 uses it as what the driver's vocal model keeps back from the
light pool's budget. Measured in a fresh process on the container, the model
and its imports held 740 MB once loaded, and scoring peaked at 1064 MB for a
four minute track and 1196 MB for an eleven minute one, the decode at the
model's rate being most of the difference.

**Measured cost.** The reserve is about 170 MB short for the longest track
measured, which the planner's headroom covers several times over. Measured
with untrained weights on Linux; the real checkpoint is the same size.

**Closes when:** the vocal pass declares its cost the way the light pass now
does, a base and a rate by the track's length, from a measurement with the
real model on the Mac. Ledger only.
