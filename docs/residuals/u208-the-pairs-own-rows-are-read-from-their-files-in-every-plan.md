---
title: A pair's linked rows with no database ISRC are read from their files in each of the three plans a sync makes whenever an account track the library lacks has a code no row's database ISRC names
found: at the review of #498, U208, 2026-11-05, round one.
issue: no
---

**The mechanism.** `here()` in `sync/pair_cli.plan_pair`, the lookup that
finds a sibling release's row among the pair's own rows, reads the audio tags
of every row with no database ISRC that the plan did not already read, once
per plan, and a sync makes three plans. `_Reader` is per plan, so nothing
carries the reads across.

**Measured cost.** Driven by the review: four linked file ISRC rows and one
hand added track the library lacks, 12 file reads in one sync; a quiet sync
reads none. Time only, proportional to the playlist's file ISRC rows; no
wrong answer.

**Closes when:** the file identities are read once per sync (a cache carried
across the gates' plans) or recorded with the link. Ledger only.
