---
title: A copyright line naming one registered label that carries no genre sends its file to the catalogues and no warning says why
found: at the review of #648, U240, 2026-11-11.
issue: no
---

**The mechanism.** `tag folder` records the label a copyright line named on the file's item report (`copyright_labels`) when that label has no genre, and asks the catalogues. The summary counts only lines naming two labels (`copyright_ambiguous`), so nothing in the envelope says a registered label without a genre was found; `--label` on such a label warns `tag-folder-label-no-genre`, the copyright path does not.

**Measured cost.** Driven by the round one review: a `℗ 2021 Gettraum` file, Gettraum registered with no genre; the item report names it, the summary and warnings do not. A person reads a file asked of the catalogues with no hint that one `crate label registry set Gettraum --genre WORD` would have tagged it.

**Closes when:** the summary counts files whose line named one label with no genre, by label, and a warning names the `registry set` command. Ledger only.
