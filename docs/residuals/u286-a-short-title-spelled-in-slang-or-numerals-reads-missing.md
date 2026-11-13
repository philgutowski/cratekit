---
title: A short title spelled in slang or numerals, Luv U for Love You or 4 U for For You, reads missing and is downloaded again
found: at the review of #830, U286, 2026-11-13.
issue: yes
---

**The mechanism.** U286 offers an approximate hit only when its folded title
resembles the wanted one on its own (`_title_resembles` in
`acquire/match.py`). A title written with a numeral or slang for whole words
shares no word with the spelled out title and scores on its letters alone:
`Luv U` against `Love You` scores 61.5 and `4 U` against `For You` 40.0, both
under the floor of 66. `Luv U` scores exactly what `Get Out` against `Agenou`
scores, so no floor separates them. A longer title sharing other words,
`I Would Die 4 U` against `I Would Die For You`, still passes.

**Measured cost.** Driven through `match run` at round one: both pairs were
offered `title-approximate` on the base and read `missing`, `not-in-library`,
on the branch, with an acquisition option, so the pass downloads a record the
library may already hold and reports it missing. Whether such a pair is the
same record is a judgement the matcher cannot make from the letters.

**Closes when:** a short vocabulary of numeral and slang spellings (`4` and
`for`, `2` and `to`, `u` and `you`, `luv` and `love`) is folded into the title
test's comparison, or Phillip decides these are rare enough to download, which
the card's Question for Phillip asks. Earns an issue: the product reports a
held track missing and fetches it again.
