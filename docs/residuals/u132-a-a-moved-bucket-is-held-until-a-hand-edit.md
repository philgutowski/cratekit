---
title: A bucket that moved out of another reaches an older copy only after a hand edit
found: at the build of #300, U132, 2026-10-10.
issue: no
---

**The mechanism.** `crate taxonomy upgrade` only adds, and holds a bucket whose
words another bucket of the copy's already files where the shipped template
does not. Soul (U118) left R&B and Hip-Hop left the non electronic bucket, so a
copy made before U118 still files their words in the old place, and both are
held. On a scratch copy of the live library's taxonomy (read only, 2026-10-10)
the plan adds `favorites`, raises `schema_version` to 4, and holds `soul` over
`'Soul'`, `'Soul / R&B'` and `'soul & funk'` in `rnb`, and `hip_hop` over the
non electronic bucket's `'Hip-Hop'`, `'Hip-Hop / R&B'` and its `hip_hop` sub
with that sub's tag words and source map. Doctor's `taxonomy.schema` and the
verb's held note name each word and where it sits.

**Measured cost.** None of it is lost or misfiled: the held buckets stay out
and every track keeps routing where it routed. What a person pays is the hand
edit, and the vocabulary row `{ word = "Soul & Funk", tag = "R&B" }` and the
`sub_by_source` rows for Hip-Hop are part of it, which the held note does not
spell out row by row. Taking R&B's Soul words out by hand and running the
upgrade again was driven on that scratch copy and adds `soul`.

**Closes when:** a reshaping verb moves a bucket's words with the bucket, or the
attended repair A36 makes the edit by hand. Ledger only: the upgrade says what
it holds and why, and A36 owns the live library.
