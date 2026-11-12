---
title: The deletion pass excuses the streaming spelling without its trailing slash, a form the live library was not measured to carry
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** `deletion.candidates._STREAMING_LOCATION` accepts
`/v4/catalog/tracks/<id>` as well as `/v4/catalog/tracks/<id>/`. The card
measured 137 live rows in the slashed form; whether every one of them matches
the pattern, and whether rekordbox ever writes the unslashed one, was not
measured from a cloud container.

**Measured cost.** None found. The unslashed form is still excused only when
nothing exists at it, and a miss lands in the refusal named under
`/v4/catalog`, the safe direction.

**Closes when:** the attended run of `crate delete review` on the live library
reads every streaming row as excused, or the pattern is narrowed to what it
counts. Ledger only.
