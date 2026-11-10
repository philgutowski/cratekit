---
title: A copyright line with a bare P or C before its year is harvested with the letter and the year in the name
found: at the review of #645, U237, 2026-11-10.
issue: no
---

**The mechanism.** `_YEAR` in `src/cratekit/label/harvest.py` strips only `(P)`, `(C)`, `℗` or `©`, as the brief asks ("and nothing else"), so `P 2021 Cadenza` reads `P 2021 Cadenza` and `C 2021 Puls` reads `C 2021 Puls`, where the old pattern read `Cadenza` and `Puls`. A letter followed by a space and a four digit year is never a name's first letter, so `[PC]\s+(?=\d{4}\b)` would strip it without clipping a name. Pinned at its current reading by `test_a_letter_after_a_mark_is_not_a_second_mark`.

**Measured cost.** Driven through `harvest.from_tracks`: the harvest offers a label under the longer name; verification is unaffected, since the needle still confirms both lines as whole words. Whether the provider ever serves a bare letter line is unmeasured.

**Closes when:** a live harvest shows such a line, and the pattern is widened to a bare P or C followed by a year, or nothing ever shows one. Ledger only.
