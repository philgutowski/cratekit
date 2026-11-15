---
title: The record's asked title is the question before Discogs sets its last bracketed mix aside
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** The sweep's record carries `asked.title`, the title read
past the head, which is what the record shops' free text query is sent.
Discogs' `_search` then sets the last bracketed group aside, as it always
has, so for `03B - 83 - On My Way (Original Mix)` the record says
`On My Way (Original Mix)` and Discogs was sent `On My Way`.

**Measured cost.** Driven at round one. A person reading the record against
Discogs' own search sees a mix the request did not carry. GUIDE now says the
mix is set aside; the record itself does not.

**Closes when:** the record carries what each source was sent, or a
`track` beside `title` for Discogs. Ledger only.
