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
Phillip answered the card's question on 2026-11-05 (decision
`533-listing-age-1`): seven days for every verb, the sweep included, as built.
What remains is that the sweep alone does not say the age.

**Measured cost.** Read, not driven, on the sweep: a release the label put out
after its listing was kept is absent from a sweep for up to seven days, and
the sweep's report does not say so. Nothing false is said; the age is
unstated there.

**Closes when:** the sweep's report carries the listing line the two verbs
print. Ledger only: the life is Phillip's choice, and nothing false is said.
