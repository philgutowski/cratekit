---
title: A history list that keeps other tracks keeps the gap a removed track's TrackNo leaves, and what rekordbox does there is unmeasured
found: at the build of #925, R-1830, 2026-11-22.
issue: no
---

**The mechanism.** #925 renumbers the members after a removed track in every
playlist `crate sync removed` takes it out of, as sitting 102 (A197) measured
rekordbox 7.2.19 doing. A history list is a different table,
`djmdSongHistory`, with its own `TrackNo`, and no sitting has removed a track
from a history list that holds other plays: A185's history list held the
removed track alone. So `rb_writer.CollectionRemoval` deletes the removed
track's history row and leaves the numbers of the plays after it as they
were, and the SQL confinement refuses any history row moving.

**Measured cost.** Not driven against rekordbox. A gap is what the history
list shows nothing for: rekordbox orders the list by `TrackNo`, so the order
of the plays is unchanged. Whether rekordbox renumbers there, and whether it
reads a gap as anything, is the measurement.

**Closes when:** an attended sitting plays two real tracks and a throwaway on
a deck so one history list holds all three, removes the throwaway with
Remove from Collection, compares the copies, and the removal imitates what it
finds. Ledger only: it closes at a sitting.
