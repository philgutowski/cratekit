---
title: A file searched only for its picture spends up to four Discogs requests, which name no picture
found: at the review of #673, U244, 2026-11-12.
issue: no
---

**The mechanism.** A file that already has a genre and no picture is still
searched, so Beatport's row can name a cover. When Beatport misses, the walk
goes on to Discogs, which is never asked for a picture, and its answer is
discarded. The searcher's signature carries no "picture only" question.

**Measured cost.** Driven at the review: four paced requests a run for each
such file, about five seconds and four of the sixty a minute. Since the fix
round such a file is not counted in the no token warning.

**Closes when:** the searcher is told when only a picture is wanted and stops
at the sources that name pictures. Ledger only: a rate budget, not a wrong
answer.
