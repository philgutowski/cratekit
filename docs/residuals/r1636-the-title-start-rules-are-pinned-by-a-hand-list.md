---
title: The title start rules are pinned by hand listed rows, and two reviewers found guards no test killed
found: at the review of #781, R-1636, rounds one and two, 2026-11-12.
issue: no
---

**The mechanism.** `tests/test_title_matcher.py` pins each rule of the title
start (`_title_starts`, `_head_end`, `_names_the_artist`) with hand listed
rows, `test_each_rule_of_the_title_start_holds` and the credit tables that
followed. Round one found six guards that killed no test, round two nineteen
of the fix round's; the rows that pin them were added in each fix round, but
a hand list names the cases its author thought of (seam rule P3) and covers
no rule a later change adds.

**Measured cost.** None to a user: a maintainer facing gap. The mutation
table, `docs/mutation/r1636.md`, reads what the rows kill.

**Closes when:** the title start rules are pinned by a generated table, every
name shape the naming verb renders crossed with the artist written each way a
credit is, checked against what the plain title matches. Ledger only.
