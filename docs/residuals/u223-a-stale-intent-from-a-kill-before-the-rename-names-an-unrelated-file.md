---
title: An intent left by a kill before analyze run's rename names an unrelated file as the twin once the source is deleted
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** `_finalize` records the rename intent before it claims
the name and renames. A process death between the intent and the rename
leaves an intent whose rename never landed. U223 drops it at the start of the
next attempt whose source is still a file, but if the source is deleted
first and another file is put at the intent's exact headed name, the resume
reads that file as this item's twin and reports it `resumed_after_rename`.
Present on main before U223, narrowed by it.

**Measured cost.** Driven by the round one reviewer: a kill after
`record_rename_intent`, the source deleted and a different file placed at
the target by the test in the person's place; resume exit 0 over the
unrelated file. Told something false, but the producer is a hard kill plus
two moves by a person into the exact name.

**Closes when:** the intent carries something that identifies the source's
content (its size and modification time, or a digest) and the twin is
accepted only when the target matches it. Ledger only.
