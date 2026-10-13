---
title: the set playlist's recorded playlist is the newest record by session id, which a second does not order
found: at the review of #307, U134, 2026-10-12, by the same shape in the refill.
issue: no
---

**The mechanism.** `set_playlist.recorded_playlist` takes the newest closed
record naming a set job, sorting by `session_id` in reverse. A session id is a
second's stamp and four random hex characters, so two records made inside one
second sort by chance. The refill's own lookup had the same shape and its
twin test failed one run in two on it, before U134 ordered records by
`started`, which carries microseconds, then by id.

**Measured cost.** Not driven for the set playlist. Two writes of one set's
playlist would have to commit in the same second for the wrong record to be
read, and a backfill run by a person does not.

**Closes when:** `recorded_playlist` sorts by `(started, session_id)`, the
order `refill.recorded_entries` uses. Ledger only.
