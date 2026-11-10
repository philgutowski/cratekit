---
title: Offers, holds and kept rosters made under the substring needle are never verified again, and an old hold can make the sweep refuse falsely
found: at the review of #645, U237, 2026-11-10.
issue: no
---

**The mechanism.** Until U237 `labels_match` confirmed a credit holding the needle anywhere, so the Rawax needle confirmed releases credited `RAWAXXX`. Whatever a sweep offered or held under that rule stays: an offer open in review is never verified again (`src/cratekit/label/sweep.py`, the offer and hold paths), a hold is filed without verification once the genre gate lets it through, which `test_a_labels_kind_changed_after_a_hold_releases_what_now_fits` pins on purpose, and a kept roster (`src/cratekit/label/kept_listing.py`) built from a `RAWAXXX` compilation keeps that act for its kept life of seven days. Worse, when the newest held releases are another act's, the next sweep reads them as releases it could not confirm and refuses with `label-sweep-incomplete`, "could not confirm a single one", naming a needle repair the needle does not need.

**Measured cost.** Driven by the reviewer on the suite's fakes: the false refusal with two old holds and one new other act release, exit 1, even with a confirmed release open in review; the kept roster reused with 84 answers and nothing offered. The live state was not read: the brief measured three `RAWAXXX` releases offered under Rawax, not held. Main alone reaches the same false refusal when a person narrows a needle between two sweeps, so this is the canary's existing assumption with a second way in.

**Closes when:** the attended card for U237 has listed and rejected the old offers and holds credited to another act, and the false refusal either cannot be reached (a hold is verified again under the current rule before the canary counts it) or is accepted as the narrowed needle case. Ledger only until the attended pass shows a live hold of this shape.
