---
title: A copyright line with an ampersand between marks, a mark after the year, two years or leading space still harvests a junk name
found: at the review of #645, U237, 2026-11-10.
issue: no
---

**The mechanism.** `labels_from_copyright` (`src/cratekit/label/harvest.py`) strips a run of marks at the very start and then one four digit year. `℗ & © 2021 Cadenza` reads `& © 2021 Cadenza`, `2021 ℗ Cadenza` keeps its mark, `(P) 2019, 2021 Cadenza` keeps a year, and a line with leading whitespace keeps its mark, because the pattern runs before the strip.

**Measured cost.** Six shapes driven by the reviewer; every one reads the same as or better than main, and none loses a confirmation, since the needle still matches the label's whole words inside the junk. The cost is a harvested name a person would reject. How often the provider serves these shapes is unmeasured.

**Closes when:** a live harvest shows one of these shapes, and the reader strips it. Ledger only.
