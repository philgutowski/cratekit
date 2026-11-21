---
title: A catalogue that is down beside one that answers is asked on every row of a suggest walk
found: at the review of #891, U322, 2026-11-21.
issue: no
---

**The mechanism.** Since U322 a row some catalogue answered ends the suggest
walk's run of unread rows, so the walk stops only when no catalogue it sends
rows to could read three in a row. U281's per catalogue count stops a
catalogue only for refusals (`searchers.Refusals`); an outage or a parse break
ends a run of refusals and has no stop of its own. So Discogs answering 503
beside a Beatport miss is asked on every row: the review drove ten rows, ten
Discogs searches where main made three.

**Measured cost.** Unmeasured in wall time: each such request waits up to the
request timeout before it is read unreachable, on top of the pacing.

**Closes when:** a catalogue unreachable on several rows in a row is passed
over for the rest of the run the way a refusing one is, with its own count
and note, or the cost is measured and found small. Ledger only.
