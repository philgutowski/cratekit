---
title: A tag folder sweep queued before R-1476 reads its --label as a name, and one queued before U240 still finds another label's genre under a shared name
found: at the review of #658, R-1476, 2026-11-11.
issue: no
---

**The mechanism.** `_folder_seam` in `src/cratekit/tagging/cli.py` answers the frozen `label_id`, which no job queued before R-1476 carries, so such a job reads its `--label` through the tag seam as a name: a name two labels share answers nothing. A job queued before U240 froze no needles, so `_frozen_labels` holds only the labels with a genre and the card's defect stands for it.

**Measured cost.** Simulated, not driven, by stripping the payload keys at queue: (a) a job frozen with the name and the needles and no identifier, `--label alpha` under two Alphas, asks the catalogues with no warning where main wrote the genre; (b) a job frozen before U240, `--label omega`, writes the other Alpha's genre. The producer is a job queued on an older build and resumed after upgrade.

**Closes when:** such jobs are gone from every queue, or the resume warns that a job froze no identifier. Ledger only.
