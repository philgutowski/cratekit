---
title: The scheduled label sweep answers from a kept listing up to seven days old, and its report does not say the listing's age
found: at the build and review of #533, U217, 2026-11-05.
issue: no
---

**The mechanism.** U217 keeps a label's listing for seven days in
`label/kept_listing.py`, and every caller of `TidalCatalogue.artist_for`
reads it, the scheduled sweep (`label.cli.handle` through
`sweep.LabelSource`) included. `label sync --next`, the walk and `label
playlists` print where the listing came from and how old it is; the sweep's
job report records only `beyond` and says nothing about the listing's age.
The brief gave the seven days; whether the sweep should list fresh instead is
a question put to Phillip on the card, options seven days everywhere (built),
the sweep always fresh, one day everywhere, or a `--fresh` flag.

**Measured cost.** Read, not driven, on the sweep: a release the label put out
after its listing was kept is absent from a sweep for up to seven days, and
the sweep's report does not say so. Nothing false is said; the age is
unstated there.

**Closes when:** Phillip answers the card's question and the chosen life is
built, or the sweep's report carries the listing line the two verbs print.
Ledger only: it is a product choice awaiting an answer, not a defect.
