---
title: A file that needs only its picture asks Discogs first, which never names one
found: at the build of #798, U282, 2026-11-13.
issue: no
---

**The mechanism.** `tag.tag_one` asks the searcher about a file that already
has a genre (its own, or its registered label's) when it has no picture,
because only its cover is wanted. The searcher's signature is `(artist,
title)`, so it cannot tell a picture-only file from one that needs a genre,
and since U282 its walk asks Discogs first. Discogs names no picture, so for
such a file its answer is spent: a database search and up to three release
reads, each paced, before Beatport is asked for the cover through the hit's
`ask_picture`.

**Measured cost.** Driven on fakes: a three file sweep with one picture-only
file sends Discogs three searches where only the two genre-needing files
needed one (U282's review, round one). A person pays time, about five seconds
of pacing per such file, and Discogs' sixty a minute budget. No wrong write,
no false report: the cover arrives as before.

**Closes when:** the searcher is told what the file needs, a keyword on the
shipped searcher or a second binder for a picture-only question, and a
picture-only file asks the record shops alone. Ledger only.
