---
title: tag retag builds its searcher per file, so it asks a refusing Beatport on every file rather than stopping after three
found: at the review of #796, U281, 2026-11-13.
issue: no
---

**The mechanism.** U281 handed `tag folder`'s worker the run's count of
refusals in a row, `searchers.for_run`. `tag retag`'s worker calls
`searchers.for_taxonomy(declared)` per file with no count, so each file's
searcher keeps its own and starts again: a Beatport refusing this client is
asked once per file, at one paced request each. `tag suggest --catalogue`
builds one searcher for its plan, so it does stop.

**Measured cost.** Not driven through `tag retag`. One paced request a file
against a catalogue that has already refused, and the answer is the same
`blocked` either way, so no file is recorded differently.

**Closes when:** `retag_cli` hands `for_taxonomy` the run's count, keyed as
`tag folder`'s worker keys it. Ledger only: a maintainer facing cost, nothing
a person reads is false.
