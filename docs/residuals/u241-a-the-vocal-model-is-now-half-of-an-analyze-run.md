---
title: The vocal model is now about half of an analyze run, and it stays one model in the driver
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** U241 moved the light head, key, tempo, drift and energy,
off the driver and made its separation about seven times cheaper. The vocal
pass was out of the card's scope and is unchanged: one model, loaded once in
the process that drives the job, scoring each track in eight second chunks
(`analysis/vocals.py`, `analysis/vocal.py`). So the driver now spends nearly
all of its time in the model, and however many light workers the machine
affords, a run cannot finish sooner than the vocal pass alone.

**Measured cost.** On the 23 track synthetic set, one process, the vocal
decode and model were 22 percent of the run before U241 (179 of 787 seconds)
and 51 percent after it (182 of 355). With two light workers on four cores
the whole run took 270 seconds, where the vocal pass alone takes 182: the
model's threads and the workers were sharing the cores. Timed on the shipped
architecture with untrained weights, since the checkpoint is not in the
container, so the seconds are a container's and the split is the finding.

**Closes when:** a unit gives the vocal pass its own run ahead, the two
workers its cap already allows at their measured cost, or shows a batched
forward pass gives the same scores; either needs the real model, so the
measurement is an attended one. Ledger only: nothing is wrong, it is what
bounds the next speedup.
