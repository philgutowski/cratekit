---
title: A restore of a landing taken after an adopt, once the adopt was restored, brings the adopted rows back and leaves the files old
found: at the review of #970, R-1924, 2026-11-23.
issue: no
---

**The mechanism.** A restore puts files back from the before values later
sessions kept, and keeps no record of the tags it wrote itself. A capture
taken after an adopt holds the adopted rows; restored once the adopt itself
was restored, it brings those rows back, and no record says the files should
carry the adopted tags again.

**Measured cost.** Driven at review round two: adopt, land a second batch,
`restore run ADOPT` naming the second landing to discard (ok, 5 of 5 put
back), then `restore run SECOND_LANDING`: exit 0, ok, `planned 0`, no
warning; the rows carry the adopted titles and the five files the old title
tag and key tag. Nothing false is said, and `analyze adopt` run afterwards
plans those files again, so it is repairable with the shipped verbs.

**Closes when:** a restore records the tags it wrote, so a later restore can
bring them forward, or says that the files were left as they are. Ledger
only: repairable by the adopt verb.
