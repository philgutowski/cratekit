---
title: A pass with a Discogs token stops when Discogs refuses too, built as the conservative call while Phillip's answer is open
found: at the build of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** Phillip's answer on #790 lets a pass carry on past refusing
catalogues only with a Discogs token recorded. The build carries a file on
only when Discogs READ it (a miss, or a match whose styles name no folder).
When Discogs refuses too (its rate limit spent, a 403, a token it rejects),
every catalogue asked refused, the item fails as before, and the pass stops
at its tag step naming each refusing catalogue. The question is on the card
under Question for Phillip, three options, the built one recommended.

**Measured cost.** Driven in `tests/test_sync_refused.py`
(`test_with_a_token_discogs_refusing_too_stops_and_names_both`). A Discogs
outage of its own holds a batch in staging until a catalogue answers.

**Closes when:** Phillip answers the card's question; option 1 closes it as
built, option 2 or 3 is a card of its own changing `_refused_by_all` and
`tagging.cli._refused_out`. Ledger only.
