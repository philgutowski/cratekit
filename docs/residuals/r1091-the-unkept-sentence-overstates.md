---
title: The warning that a full label build's reads could not be kept says all of them when an earlier write kept some, and names the temporary file
found: at the review of #410, R-1091, 2026-11-01.
issue: no
---

**The mechanism.** `KeptReads.flush` in `src/cratekit/label/kept_reads.py`
records the last write that failed as `unkept`, and the build gate's screen
and the warning `label-playlists-reads-unkept` say "the reads made by this
run could not be kept ... so a later run reads them again". The document is
written whole, so a periodic write that succeeded before a later one failed
has kept the reads up to it, and the sentence overstates how many the next
run repeats. The error text is the operating system's, which names the
temporary file beside the document rather than the document itself.

**Measured cost.** Driven at round 2: `FLUSH_EVERY` two, the first write
succeeding and the later ones refused with a full disk; the store held two
reads, the next run reused those two and asked for the other four, while the
screen had said none were kept. Calls only; nothing a person does differently.

**Closes when:** the store counts the reads its last successful write held,
and the sentence says how many were kept and how many were not, naming the
document's path.
