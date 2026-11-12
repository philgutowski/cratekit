---
title: The excluded anchor refusal's pass over a folder it cannot read is a guard no test reaches
found: at the review of #779, U279, 2026-11-12.
issue: no
---

**The mechanism.** `Exclusion.holder` in `modules/tools/setbuilder.py` reads
each folder above an anchor by its identity and passes over one it cannot
`stat` (`except OSError: continue`), so an anchor under a missing folder
inside download staging is still placed in staging. Changing the pass to
`return None` kills no test: the anchor then takes the general not indexed
wording rather than the one naming the staging folder.

**Measured cost.** Wording only, driven at round two of the review with an
anchor at `<root>/Downloads/gone/x.flac`: the slug and the exit code are the
same either way, and the general wording also says the index leaves the
staging folder out. Nothing is lost.

**Closes when:** a test plants an anchor under a folder that does not exist
inside an excluded folder and asserts the refusal names the folder. Ledger
only.
