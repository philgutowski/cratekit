---
title: tag retag and tag suggest ask an untagged file with no artist, since only tag folder reads a name's artist
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** The question's title is read in the catalogue searcher,
so `tag retag` and `tag suggest` ask every headed title past its head as
`tag folder` does. The name's artist is read only in `tag.tag_one`, the one
caller that knows a name from a title tag; `retag.py` reads `artist` and
`title or stem` as before and `suggest.py` asks by the database row's
artist and title. An untagged file there is still asked with no artist,
which no catalogue on the walk can match.

**Measured cost.** Read, not driven. Not a regression: main asked the same
files with no artist and the head too. A retag candidate carries a genre,
so it was tagged once, and is rarely untagged.

**Closes when:** retag reads the name's artist the way `tag_one` does, or a
count shows no untagged file reaches either verb. Ledger only.
