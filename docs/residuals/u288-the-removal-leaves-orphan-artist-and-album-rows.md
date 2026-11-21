---
title: crate sync removed leaves an artist or album row the removed track was the last to name, which rekordbox's removal deletes
found: at the build of #839, U288, 2026-11-21.
issue: no
---

**The mechanism.** A178 and A185 measured rekordbox deleting every live artist
and album row a removal leaves named by nothing, the one it just orphaned and
any other already orphaned. The removal deletes in its seven measured tables
only and leaves those rows; rekordbox sweeps them at its own next removal, as
A178 saw it sweep an older orphan. Genre and label rows were never measured.

**Measured cost.** None driven: an orphan lookup row is invisible in rekordbox's
track list, and a landing that mints the same word reuses a live row rather
than minting another.

**Closes when:** the orphan sweep is measured for genre and label rows too and
imitated under the confinement, or it is left to rekordbox for good. Ledger
only.
