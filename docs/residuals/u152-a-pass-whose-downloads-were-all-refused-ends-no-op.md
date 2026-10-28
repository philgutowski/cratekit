---
title: crate sync land ends no_op with exit 0 when every download was refused for good
found: at the review of #333, U152, 2026-10-28.
issue: no
---

**The mechanism.** The brief makes a download refused for good (a lossy only track) recorded and skipped, never fatal. When every track of the list is refused, `_download` in `src/cratekit/cli/sync_land.py` ends the pass with outcome `no_op` and exit 0, a failing `sync.land.download` row naming the count, and the `sync-land-download-refused` warning naming each track.

**Measured cost.** Driven (`test_every_download_refused_lands_nothing_on_a_failing_row`). The rows a person reads are honest; a wrapper that reads only the exit status or the outcome sees a clean pass that acquired nothing. `doctor` sets the same precedent, failing rows on an OK outcome. Whether an all refused pass should exit non zero is a product call, left as it is.

**Closes when:** the `/crate-sync` wrapper (#355, U174) decides how it reads a pass, and the outcome is made to match. Ledger only.
