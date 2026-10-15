---
title: The landing's gate asks to move files into the library when the only write is owned hearts joining All Favorites
found: at the review of #325, U146, 2026-10-15.
issue: no
---

**The mechanism.** A landing whose staging is empty and whose pass has owned
hearts All Favorites lacks asks `intake.land.native`, whose prompt in the
registry reads "Move these files into the library and add them to the
collection?". The screen beside it (`backfill.landing_facts`) says
`files to land: 0` and lists the hearts by month, so what is written is
shown, and the prompt's sentence is the one line that is wrong.

**Measured cost.** Driven:
`test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
answers that gate with no file staged. A person reads a question about files
over a plan with none.

**Closes when:** the prompt names the hearts as well as the files, or the
owned only path gets a prompt of its own. Ledger only, a wording fix.
