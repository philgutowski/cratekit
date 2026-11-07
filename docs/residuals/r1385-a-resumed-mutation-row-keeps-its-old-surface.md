---
title: A mutation row reused by the driver's resume keeps the surface, description and pairing it was stored with, not the row file's
found: at the mutation table of #600, R-1385, 2026-11-07.
issue: no
---

**The mechanism.** `measure_batch` in `scripts/mutate.py` reuses a stored row under `--resume` when its fingerprint matches, and the fingerprint covers the id, file, old text, new text and kind only, as it should, since nothing else changes the measurement. But the reused result is rebuilt whole from the sidecar, `RowResult(**cached)`, so the row file's current `surface`, `description` and `pairs_with` are dropped for what the earlier run stored.

**Measured cost.** R-1385 read two zero rows, M3 and M5, as maintainer facing in its row file at 64ebdc11 and ran the driver with `--resume`: the table at 9c564d02 still listed both as user facing, each "USER FACING ZERO WITH NO COMPOSITE", with their old descriptions. The two rows were taken out of the sidecar and measured again. A row reclassified or given a composite and then resumed reads as the opposite of what its author wrote, in either direction: a row reclassified as user facing would lose the composite it now owes.

**Closes when:** a reused row takes its counts from the sidecar and its surface, description and pairing from the row file, with a test that resumes a row whose surface changed. Ledger only; the workaround is a run without `--resume` or the row's entry removed from the sidecar.
