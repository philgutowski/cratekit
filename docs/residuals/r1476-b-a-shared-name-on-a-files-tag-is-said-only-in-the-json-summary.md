---
title: A file whose label tag names a display name two labels share is asked of the catalogues with no warning, and the resume's warning names the shared name alone
found: at the review of #658, R-1476, 2026-11-11.
issue: no
---

**The mechanism.** `_label_seam` in `src/cratekit/tagging/cli.py` answers nothing for a tag naming a display name two frozen labels hold, in any case or slug spelling, by R-1476's rule. The genre label's own files carrying that name then go to the catalogues. `tag-folder-label-tag-outranked` fires only on a sweep given `--label`, so a sweep given none says it only in the JSON summary's `label_tags`. `tag-folder-label-on-resume` names the frozen label by display name alone, where the queue's warning names `Alpha (omega)`.

**Measured cost.** Driven at both review rounds: two labels called Alpha, the genre label's three fetched files tagged `Alpha`, no `--label`: no genre written, `label_tags {'Alpha': 3}`, warnings empty. On main the first holder's genre was written, the right one for these files and the wrong one for the other label's. Nothing false is said.

**Closes when:** a sweep warns when a file's tag names a display name more than one label holds, and the resume warning names the identifier beside a shared name. Ledger only.
