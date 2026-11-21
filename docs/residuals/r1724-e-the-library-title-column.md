---
title: tag suggest and tag backlog ask by the library row's title, which this unit does not read past a _PN tail
found: at the review of #883, R-1724, 2026-11-21.
issue: no
---

**The mechanism.** `tag folder` and `tag retag` read a file with no title
tag by its name through `titles.name_title`. `tag suggest --catalogue` and
`tag backlog --catalogue` ask by the rekordbox row's Title column
(`suggest.catalogue_lookup`), so a row whose Title carries `_PN` is asked
with it: handed `06A - 126 - Sean Doron - Sunshine Hotel_PN`, the shipped
searcher asks Discogs `Sunshine Hotel_PN`. Whether rekordbox writes a file's
name into Title for a file with no title tag was not driven.

**Measured cost.** Driven to the question only, at round one; the library's
Title column was not read.

**Closes when:** an attended sitting counts library rows whose Title ends in
`_PN`; none closes it, any earns a card reading the column through
`name_title`. Ledger only.
