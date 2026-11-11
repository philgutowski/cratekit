---
title: A foreign file at a path the pass's own download once recorded reads as the pass's own
found: at the review of #665, R-1499, round one, 2026-11-11.
issue: no
---

**The mechanism.** `intake.beside.beside` reads a file as the batch's own when its path is one of the batch's downloads' recorded artifacts. After the pass's tail renamed its `101.wav`, a plain download of the same track id staged a new `101.wav` at that path, and the continued pass read it as its own and named no download.

**Measured cost.** Driven at round one (d11) with the suite's renaming stand in, which overwrote the pass's renamed file; the real `name apply` is expected to stop on the taken name with U212's second copy step, which was not driven. Whether the real tail lands the foreign file is unmeasured.

**Closes when:** an own artifact path counts as own only when it is not also another download's later artifact, or carries the identity the own download recorded. Ledger only.
