---
title: inbox refill fills a native landing's later partial playlist when the pass's first and whole mirror was landed by intake file
found: at the review of #356, U175, 2026-11-01.
issue: no
---

**The mechanism.** `refill.locate` takes the oldest playlist a record names by
identifier before it asks any name. When the first landing of a pass came by
intake file (recorded with no identifier) and a later one natively (by
identifier, its ` 2` holding only its new files), the ` 2` is the one filled
`BY_RECORD` with the whole account playlist, and the first mirror is passed
over. The record first rule is U134's and unchanged by U175.

**Measured cost.** Driven by Fable's round 2 on hand built records (S2d): the
gate plans five additions into the ` 2`. Reaching it needs a cutover between
two landings of one pass, which was not driven.

**Closes when:** the oldest landing of the pass is chosen across both kinds of
entry, by start time, before the record or the name decides.
