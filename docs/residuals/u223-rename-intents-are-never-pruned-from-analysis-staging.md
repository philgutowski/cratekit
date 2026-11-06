---
title: Every renamed analyze run item leaves its rename intent in the job store's analysis staging for good
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** Since U223 `staged_path` keeps `rename-intent.json` so it
outlives the attempt that renamed the file, and the engine's commit moves
only the staged report. Nothing removes the intent once the row is done, so
`analysis-staging/<job>/<ordinal>/rename-intent.json` stays for every renamed
track, as the empty staging directories did before.

**Measured cost.** Driven by the round one reviewer: a one item run to done
leaves the staging directory listing only the intent. A small file per
renamed track; no reader is harmed, since a done row is never driven again.

**Closes when:** a job store prune removes the staging of a finished job, or
the commit hook drops the item's staging once its row is done. Ledger only.
