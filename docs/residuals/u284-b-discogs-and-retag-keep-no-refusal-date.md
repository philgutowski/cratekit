---
title: The refusal record keeps no date for Discogs, and tag retag and tag suggest never move it
found: at the build of #790, U284, 2026-11-13.
issue: no
---

**The mechanism.** The record of when a catalogue began refusing is written
only through `searchers.Refusals(record=True)`, the `tag folder` worker's run
count (`searchers.for_run`). Discogs is never under that count (U244 keeps its
own memory of a refusal in the asker), so a Discogs that refuses too is named
in a pass's stop with no date. `tag retag` builds a searcher per file and `tag
suggest --catalogue` a count of its own, neither recording, so a catalogue
that answers or refuses there leaves the record as the last sweep left it.

**Measured cost.** Driven in `tests/test_sync_refused.py`
(`test_with_a_token_discogs_refusing_too_stops_and_names_both`): Discogs is
named refusing with no date. A stale date after a retag that met an answering
Beatport was not driven; the next sweep's first answer clears it.

**Closes when:** the Discogs asker's refusals and answers move the record, and
the retag and suggest searchers record through a run count of their own.
Ledger only.
