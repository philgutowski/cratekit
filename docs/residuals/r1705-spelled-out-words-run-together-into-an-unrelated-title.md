---
title: Spelled out slang words can run together into an unrelated title, which is offered for review
found: at review round one of #833, R-1705, 2026-11-15.
issue: no
---

**The mechanism.** `match._agree` and `LibraryIndex.spelled_alike` compare
two titles with each word of `_SPELLED_OUT` spelled out and the spaces gone,
because `2 Nite` is `Tonight`. So a few listed letters run together into an
unrelated word: `B Side` against `Beside`, `C Saw` against `Seesaw`, and the
single letter titles `Y`, `C`, `R` and `N` against `Why`, `See`, `Are` and
`And`, by one artist, are offered for review where main read them missing
(driven through `resolve_one` and `crate match run` for the artist `Moby`).
`two` and `four` were taken out of the list in fix round one for the same
reason (`Two Day` against `Today`).

**Measured cost.** One wrong question per such pair, and the row waits on
it rather than downloading. Nothing is called owned. How often a real
library holds such a pair by one artist is unmeasured; `B Side` against
`Beside` was already offered on main wherever the discovery score reached
it, since their letters score 83.

**Closes when:** a sitting's version-match queue is read for
`title-approximate` items that a spelled out join made, and either none is
found or the join is limited (spaces kept, with only listed multi word
forms such as `2 nite` joined). Ledger only.
