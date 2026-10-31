---
title: A vocal sub kept under another name makes a whole vox landing file nothing
found: at the review of #346, U165, 2026-10-31.
issue: no
---

**The mechanism.** `adopt.plan.predicted_place` predicts a row given the vox
tag into its bucket's vocal sub. When the library keeps that vocal sub under a
name other than the declared one, the plan after the commit answers
`VOCAL_RENAMED` for it, `Predicted.of` reads that as no vocal sub, and the row
differs from its prediction. `intake.filing.file_landed` then files nothing for
the whole batch and warns `landing-filed-differently`, so the band memberships
that could have been filed wait for `crate adopt apply` too.

**Measured cost.** Traced, not driven: no producer of a renamed vocal sub
beside a vox landing was built. The outcome is conservative and the warning is
true, so nothing is lost and nothing is misreported.

**Closes when:** the prediction reads the tree's vocal standing on the plan's
handle, so a renamed sub is shown before the answer, or a renamed vocal sub
files the band and leaves only the vocal membership to `adopt apply`. Ledger
only.
