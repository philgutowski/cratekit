---
title: An intake landing predicts a two genre track's first folder only
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** Intake's filing prediction (`intake/filing.py`) reads one
plan entry per track, its first genre's. A landed track whose file already
carries a second genre is filed into the second folder at the next
`adopt apply`, which the landing does not say.

**Measured cost.** Not driven: a downloaded file carrying a SecondGenre tag
needs a person to have written one before the landing. Nothing is lost; the
second folder follows one verb later.

**Closes when:** the landing's report names the second folder too. Ledger only.
