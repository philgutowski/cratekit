---
title: Two guards of U284's refusal record and refusal words are reached by no shipped caller and kill no test
found: at the review of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** `refused._change` catches `RecursionError` beside `OSError`
and `ValueError`, but `read` already absorbs a record nested past the parser's
depth inside `_parse`, and `_write` writes a flat document, so the catch is
never reached. `searchers._beside_refusals` returns the token's refusal
unchanged when no outcome was gathered, which only a walk naming Discogs alone
produces, and only a direct caller can name one.

**Measured cost.** Mutations at review round two: removing either kills no
test. One candidate driven for each (a nested record; the default walk), and
neither reaches the guard. No user facing cost.

**Closes when:** the dead catch is removed or a producer is found and pinned.
Ledger only.
