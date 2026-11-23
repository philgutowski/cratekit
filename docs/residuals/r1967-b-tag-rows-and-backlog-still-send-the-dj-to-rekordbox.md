---
title: tag rows, tag backlog and tag campaign still send a word with no genre row to rekordbox, though tag set now makes the row
found: at the review of #1008, R-1967, round one, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/rows_cli.py` (`_left`), `tagging/backlog.py` (`settle`) and `cli/verbs/tag_campaign.py` advise, for a word with no genre lookup row, to give one track that genre in rekordbox, which makes the row, and then run again. Since R-1967 `crate tag set GENRE` makes the row on the commit that links it, so the hand step is no longer the only way.

**Measured cost.** Driven by the reviewer: `tag rows` left a row `genre-unknown` with that advice, and `tag set "Afro House"` on the same row then made the row and linked it. Each sentence is still true, nothing is lost and nobody is blocked; a DJ is sent to a hand step in rekordbox the product no longer needs, and a cloud session cannot take it.

**Closes when:** the three advisories name `crate tag set GENRE --row CONTENT_ID` beside the rekordbox step, or those verbs make the row as `tag set` does, which would widen the creation guard again. Ledger only: a wording change.
