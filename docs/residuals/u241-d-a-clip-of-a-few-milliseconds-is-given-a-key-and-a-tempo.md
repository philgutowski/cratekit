---
title: A clip of a few milliseconds is given a key and a tempo, and librosa's own separation does not repeat itself under a third of a second
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** `detect.analyse_file` returns `skipped-unanalysable` only
when the tempo estimate is None or a step raises. A nine millisecond clip has
an onset envelope of one frame, the tempogram still has a strongest bin in
the window, and the chroma of a clip that short still has a largest
correlation, so the detector answers a key and a tempo for it (driven: 400
samples at 44100 read 6A at 152, on the base and on the branch alike).
Separately, `librosa.effects.harmonic` over a clip of two or three frames
returned numbers on one call and not a number on the next, because scipy's
rank filter is unreliable on a line shorter than half its window; the base
detector's answer for a clip of 23 to 46 milliseconds therefore changed from
run to run. U241's separation takes those lines by the definition, so the
branch's answer is one answer, but it is still a key for a click.

**Measured cost.** A file that short in a DJ's folder is a broken download or
a placeholder, and it would be renamed with a head. Seven clip lengths were
driven; no real file was.

**Closes when:** the detector refuses a decode shorter than a floor it can
defend, a few seconds, as `skipped-unanalysable`. Ledger only until a real
file produces it.
