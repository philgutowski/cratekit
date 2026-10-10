---
title: A native plan opens each added file's tags twice, once for the title and once for the score
found: at the review of #296, U127, 2026-10-10.
issue: no
---

**The mechanism.** `native.plan_rows` reads each file's title through
`ingest.file_meta`, and `_vox_plan` then reads `voxlevel` through
`tags.read_vox_from_file`, a second container open. `tags.read_tags` reads
several fields in one open, and `file_meta` does not expose it.

**Measured cost.** Not measured. One extra open per added file per plan, and
a landing plans twice, once for the gate and once at the apply. The batches
landed so far are tens of files on the library volume.

**Closes when:** `file_meta` reads `voxlevel` in its own open and the plan
takes it from there, or a timed landing of a large batch shows the open is
noise. Ledger only, a cost and not a defect.
