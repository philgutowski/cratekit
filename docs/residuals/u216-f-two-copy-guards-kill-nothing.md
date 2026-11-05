---
title: Two guards in U216's copy check kill no test
found: at the review of #530, U216, 2026-11-05.
issue: no
---

**The mechanism.** In `sync/pair_cli._discovered_back` the copy check leaves
a playlist's own title out of the fresh titles it compares against
(`other_id != account_id`), and picks its words by whether the copied title is
paired. Removing the exclusion, or forcing the words to the brought in side,
leaves the suite green.

**Measured cost.** None driven. The exclusion matters only for a root folder
literally named `DOWNLOADED`, since a title cannot otherwise copy itself once
`name_of` strips the folder prefix; the paired side of the words is pinned by
no test.

**Closes when:** a test drives each. Ledger only, a maintainer facing guard.
