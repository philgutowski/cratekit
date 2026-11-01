---
title: The tail's vocal rescore row says it scored the files it queued, not the files it wrote
found: at the review of #378, U181, 2026-11-01.
issue: no
---

**The mechanism.** `cli/tail.py` `rescore` reports "scored the N staged file(s)" from the number of items the `analyze vocals --unscored` job held. When the model passes the probe and then fails to load (a checkpoint of the right size that will not deserialize), every item settles inactive with `vocal-model-unavailable`, the job succeeds, and the row reads ok over files that still carry no voxlevel.

**Measured cost.** Driven by the review with a loader bound that raises on load, the one way a container with no torch reaches it: the row said scored 1 and the file carried no score. The child's own `vocal-model-unavailable` warning rides beside the row on the same envelope, so the report is not clean, only the row overclaims. A real failing checkpoint on a torch machine was not driven.

**Closes when:** the row counts the job's reports by status, scored and unchanged against inactive, and says the inactive ones by reason. Ledger only.
