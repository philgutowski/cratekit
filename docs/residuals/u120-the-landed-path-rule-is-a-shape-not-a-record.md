---
title: The backfill tells a landed heart from a filed one by where its file sits, a shape and not a record
found: at the build of #277, U120, 2026-10-10.
issue: no
---

**The mechanism.** `landing.is_landed_path` says a file is one a landing put
down when it sits directly in a folder under the music dir, which is where
`landing.target_dir` puts every batch and where nothing the source system
filed sits, its files being two or more folders deep under
`Processed_Tracks`. The intake records could not answer instead: a bridge
landing's record names only its intake file, and a native landing whose every
file an account playlist claimed records no batch playlist, so neither names
the batch folder for every landing. A file somebody drops into a new folder
directly under the music dir by hand reads as landed, and a landed file
somebody moves deeper reads as filed.

**Measured cost.** None on the live library as read on 2026-10-10: every
folder directly under `Music` is a batch or the source system's own roots,
and every landed heart sits in one. The rule is wrong only for a hand move.

**Closes when:** every landing records its batch folder on its session
record, both media, and the backfill reads the records. Ledger only.
