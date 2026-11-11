---
title: Tag folder's human screen shows the job and its item count and none of the tagging summary, so the per file report is read only with --output json
found: at the build of #648, U240, 2026-11-11.
issue: no
---

**The mechanism.** `crate tag folder` renders a succeeded sweep as its job line and `items: N of N settled`, plus warnings; the `tagging` summary under `progress` (counts by source, by label, and since U240 each file by label, by catalogue or not at all) is in the JSON envelope only. True before U240; U240 added the per file list there, and a refusal's message now counts the files by way.

**Measured cost.** Driven at the build through the human renderer: a mixed folder's success shows no line saying which files a label tagged. A person reads the per file report with `--output json`, as the cutover record already did for U178's counts.

**Closes when:** the human screen renders the tagging summary's counts, by way and by label, under the job line. Ledger only.
