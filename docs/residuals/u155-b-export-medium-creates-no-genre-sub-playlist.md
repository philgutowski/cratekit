---
title: The export medium of route inbox creates no genre sub playlist, so a Rominimal track is filed into its band alone and every run warns sub-playlist not found
found: at the review of #336, U155, 2026-11-01.
issue: no
---

**The mechanism.** On the export medium `route inbox --export` creates a
folder's vocal sub before it routes (`_vox_subs`), and nothing creates a genre
sub. With no `Rominimal` playlist in the export's Minimal / Deep Tech folder
the write skips that placement with `route-write-skipped: sub-playlist not
found: Minimal / Deep Tech/Rominimal`, and the next fresh export plans the same
again. Since U155's first fix round the gate shows that placement in its
`genre` column, so the skip is said on the same run.

**Measured cost.** Driven by the review on a disposable export: the track
lands in its band only, with the warning, every run, until a person makes the
playlist by hand. Reachability on the live library is unmeasured, since its
tree has cut over to the database, where the rebuild engine creates the
playlist.

**Closes when:** the export sweep creates a declared genre sub the way it
creates a vocal sub, named among the subs it created, or refuses before the
gate. Ledger only.
