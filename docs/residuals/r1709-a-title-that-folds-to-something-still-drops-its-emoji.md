---
title: A title that folds to something still drops its emoji and marks, so Sun with one emoji is owned by Sun with another
found: at review round one of #834, R-1709, 2026-11-14.
issue: no
---

**The mechanism.** `match.fold` takes every mark and emoji off a title, and
#834 reads a title's own text only when the fold is empty. A title with a
letter or digit beside its emoji, `Sun 💧`, folds to `sun`, the same as
`Sun 🔥`, so every comparison and identity reads the two as one recording.

**Measured cost.** Driven by the review through `resolve_one`: a wanted
`Aurora Bloom - Sun 💧` against a held `Aurora Bloom - Sun 🔥` resolves
`matched`, `exact`, so the wanted track is never downloaded. How many live
titles differ only in a mark or an emoji is unmeasured. Folding marks is
deliberate (`Sun Path!` and `Sun Path` are one record far more often than
two), so the line between a decoration and a title's meaning is a product
decision, not a bug fix.

**Closes when:** a rule says when a mark or emoji beside letters names a
different record, with the live count read first. Ledger only: the cost
needs two releases by one artist whose titles differ only by an emoji.
