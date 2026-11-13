---
title: A short title a letter or two away from an unrelated one by the same artist is still offered as approximate
found: at the review of #830, U286, 2026-11-13.
issue: no
---

**The mechanism.** U286's title test, `token_set_ratio` of the folded titles
against `APPROXIMATE_TITLE_FLOOR = 66` in `acquire/match.py`, keeps every one
letter change of a three letter title, which scores 66.67. Unrelated short
titles one or two letters apart score as high: `Joy` against `Boy`, `Tique`
against `Time`, `Love` against `Alive`, `Light` against `High`, `Gold`
against `Glide`.

**Measured cost.** Driven through `match run` at round one: each is still
held `title-approximate` beside an unrelated song, the card's original cost,
a question a person rejects. Over 110 common single word titles under 8
artists, 1,088 pairs sharing no word and clearing the discovery floor are
still offered. The base offered every one of them too, so U286 narrows the
class rather than causing it.

**Closes when:** a floor that scales with the title's length separates a
one letter change in a three letter title from two letters changed in a
four or five letter one, measured on the same pairs. Ledger only: a question
a person can reject costs no file and no row.
