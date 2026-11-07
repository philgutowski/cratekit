---
title: Three of the guards on what a sync pair reads as owned kill no test, sampled by U229's mutation table
found: at the mutation table of #593, U229, 2026-11-07.
issue: no
---

**The mechanism.** In `src/cratekit/sync/pair_cli.py`, `landed_inbox_playlists` reads a landing still awaiting its import as a landing (U128), and `_owned_by_jobs` reads only a SUCCEEDED job and only an `owned` report (U130). Each was removed alone by U229's table, rows S3, S4 and S5, and no test in the suite died.

**Measured cost.** None measured. An intake file's landing entry carries no playlist id, an unfinished job's reports may not read, and a report in another state may carry no path, so each removal may be equivalent on every input the suite builds; no input that would show otherwise was driven.

**Closes when:** each guard has a test that fails when it is removed, or a measurement shows the removal equivalent. Ledger only: a maintainer facing gap in pinning.
