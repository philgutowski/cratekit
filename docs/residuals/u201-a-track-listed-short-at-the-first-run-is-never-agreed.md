---
title: A genre track the account listed short at the first U201 run is never agreed on its playlist, and can later be read as a person's addition and filed back
found: at the review of #489, U201, round two, 2026-11-05.
issue: no
---

**The mechanism.** The snapshot of a mirrored genre playlist is what the account
listed when the mirror finished it (`mirror_edits.agreed_after`, recorded by
`mirror.apply` and `mirror.settled`). A track the provider counts and does not
list, an unplayable one, is absent from that listing when the first U201 run
records the playlist, and the mirror's add of it reads back absent, so it is
recorded as refused and never agreed. If rekordbox later takes the track out of
the tree and the provider lists it again, `mirror_edits.decide` reads it as on
the account and not in the snapshot, a person's addition, and the rekordbox
area's `mirror-edits` step files it back into the playlist.

**Measured cost.** Driven by the round two reviewer on the strict fake, with the
fake's `add_tracks` answering as `tidal_account.add_tracks` does for a hidden
track (scratchpad drive S13): a removal made by hand in rekordbox is undone by a
write and the gate names an account edit nobody made. The producer, the
provider listing a once unplayable track again, was not driven; one candidate
was driven on the fake and produces it. Ledger only for that reason.

**Closes when:** a track the mirror asked to add and the provider refused is
read as agreed absent rather than unknown, for instance by recording the refused
track in the snapshot's own word, with a test of the S13 sequence.
