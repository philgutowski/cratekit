---
title: Whether a release's copyright line names a label is decided by three copies of one rule
found: at the review of #646, U238, 2026-11-10.
issue: no
---

**The mechanism.** `sweep._past_window`, `tidal_catalogue._credits_label`
and the provider's `search_release` judged by `verify.verify_release` each
pair `harvest.labels_from_copyright` with `verify.labels_match`. The sweep
does not import `_credits_label` because it lives in the provider adapter,
which the generic sweep must not import, and it needs a third answer, no
line, that `_credits_label` folds into no. A repair to one copy (U237's
extractor fix lands in the shared extractor, so it reaches all three) that
changed the match itself in only one would let the count past the window
drift from what the window confirms.

**Measured cost.** None today: round one's review classified 20 line
shapes by the count and by the window's verifier and they agreed on 20 of
20. Argued from reading only.

**Closes when:** one public function in `cratekit.label.verify` or
`harvest` answers yes, no or no line for a release and a needle, and all
three callers use it. Ledger only.
