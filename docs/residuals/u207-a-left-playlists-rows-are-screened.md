---
title: The account mirror screens the ISRCs of a playlist its plan then leaves, a person's playlist of the same title
found: at the review of #497, U207, 2026-11-05.
issue: no
---

**The mechanism.** `organize.account_mirror.read` hands `Matcher.screen` every row of every mirrored folder before any plan runs. A playlist the plan then leaves, because a person's playlist of the same title already sits in the folder, has its rows screened though none of them is ever matched. Rows with no database code also have their file's tag read for the screen.

**Measured cost.** Driven by the round two review on the mirror's fixture world: a library mirroring one playlist that the account already holds under a person's title planned no match and screened all three codes. With the app client that is one batch request per twenty such rows where `main` sent none. It costs request budget only: no data and no false report.

**Closes when:** the screen runs per folder after the plan has decided which playlists it reuses or creates, or the rows of a left playlist are left out of it. Ledger only.
