---
title: The label tombstone question's judgement of undated releases and the unmapped prefix fallback kill no test
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** Two guards the round one review mutated killed nothing and
were not pinned in the fix round: `playlists_cli._group` judges a removed
track on every release, dated or not, and judged on dated releases only the
suite stays green, since an undated release is never planned into a year; and
`candidates.reference_set` names an unmapped row with no prefix as "an
unreadable prefix", a branch the resolver cannot reach, since it answers
`UNMAPPED` only for an absolute path.

**Measured cost.** None today. The undated judgement matters only for a track
recorded on a year before its release lost its date.

**Closes when:** each is pinned by a test or taken out. Ledger only.
