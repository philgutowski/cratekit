---
title: U166 landed by a local merge pushed to main, not through the pull request U158 asks for
found: at the landing of #347, U166, 2026-10-28.
issue: no
---

**The mechanism.** U158 landed on `main` while U166 was being built, and from
it a unit reaches `main` through a pull request its session opens and merges
once CI on its head is green. This session's own instruction, written before
U158, said to merge to `main`, push `main` and open no pull request, and the
harness forbids a pull request nobody asked for. The conservative call was to
follow the session's instruction: the same merge commit and trailer, merged
locally and pushed, which is the fallback U158 names for a refused merge
endpoint. The battery was run on the merged tree before the push; CI judged
it after.

**Measured cost.** None to a person: the merge commit, its trailer and the
battery are what a pull request would have carried. The record a pull request
holds is in the card's Landed comment instead.

**Closes when:** the scheduled task's prompt that starts cloud workers is
brought in line with U158, so a worker's instruction and the repository's
rule agree. Ledger only.
