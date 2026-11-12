---
title: A credit written with no separator after its marker, such as (feat_Mira) or (featMira), now reads as a version
found: at the review of #691, U262, 2026-11-12.
issue: no
---

**The mechanism.** `acquire/match.py` `_is_a_credit` now asks the group's
first whole word under the matcher's `fold`. `fold` keeps an underscore and
any letter as part of a word, so `(feat_Mira)`, `(featMira)` and a marker run
straight into a name in another script have no first word equal to a marker,
and the group is kept as the version. The letters rule read them as credits.
`core/tombstone.py` already read them as versions, so the two modules now
agree on them.

**Measured cost.** Driven through `read_text_lines` and `resolve_all` against
a library holding only the plain `Sun Path`: `Sun Path (feat_Mira)` was
matched exact on the base and is `needs_review`, `version-differs` on the
branch. The cost is a question rather than a wrong ownership, the
conservative direction. None of the 58,222 distinct bracketed groups in the
repository's text is a real credit of this shape, so the reachability is
unmeasured.

**Closes when:** a live list shows such a spelling, and the rule learns to
read a marker followed directly by a name in both modules together. Ledger
only.
