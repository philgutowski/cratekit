---
title: A track the provider refused once is never offered to its mirrored playlist again
found: at the review of #326, U147, 2026-10-15.
issue: no
---

**The mechanism.** `mirror.apply` records a track `add_tracks` did not hold
under the playlist's `refused` (`ledger.record_mirror_refused`), and
`mirror.plan` leaves every recorded refusal out of a refresh's adds, the label
folders' rule, so a refresh over an unchanged playlist plans nothing. Nothing
ever clears the entry, so a track that was region locked or briefly withdrawn
and later becomes playable stays off its mirror.

**Measured cost.** Driven with the fake's `unaddable`: the second plan is
`nothing` and the gate item says `refused before: 1`. The mirror then differs
from rekordbox by that track, said on every plan, never silently. Retrying
every run instead would keep the step planned for ever over a withdrawn track.

**Closes when:** a refresh retries refused tracks on some cadence, or a verb
clears one playlist's refusals. Ledger only.
