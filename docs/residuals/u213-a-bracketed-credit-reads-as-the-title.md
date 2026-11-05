---
title: A title that is only a bracketed credit or qualifier reads as the title, and a set aside track shows its own spelling beside the word no title
found: at the review of #507, U213, 2026-11-05.
issue: no
---

**The mechanism.** U213 made a bracketed group that is all a title has left
the title (`acquire/match.py` `split_version`), so `[Premade Sandwiches]`
reads. The rule takes no exception: a row titled only `(feat. Mira)` reads as
the title `feat. Mira`, `(Original Mix)` as `Original Mix`, `(Live)` as
`Live`, where `main` refused each as naming no title. An exception for
credits was built in round one and taken out in round two, because the
credit prefixes include `with ` and `[With You]` and `(With Or Without You)`
are titles. Separately, a track `crate sync twins` sets aside is named on the
gate by the title its row spells, so a row titled `[]` shows as
`Nova Reef - [] (the account lists it with no title, ...)`.

**Measured cost.** Driven on the reader: each of those spellings reads as
described. No provider row titled only by a credit or a qualifier was found
or driven, so the reachability is unmeasured. Where one exists it is queued
and matched under that word as its title rather than refused, a narrower
cost than the whole playlist refusal it replaced. The gate line is wording;
nothing false is written.

**Closes when:** a live listing shows such a row, and the rule is narrowed to
the guest credit prefixes that cannot begin a title (`feat`, `ft`,
`featuring`) with a test per prefix. Ledger only.
