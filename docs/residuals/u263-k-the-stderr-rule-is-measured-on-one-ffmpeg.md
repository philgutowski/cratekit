---
title: The rule that any ffmpeg error about the audio fails a decode is measured on ffmpeg 6.1 only
found: at the review of #692, U263, round two, 2026-11-12.
issue: no
---

**The mechanism.** `decode._ffmpeg_samples` fails a decode when ffmpeg at
`-v error` says anything not from its three cover decoders, on the measured
ground that a clean decode says nothing. A later ffmpeg that logs a benign
line at that level, or names its cover decoder differently, would refuse a
playable M4A as `skipped-undecodable`, or keep a cover complaint as a fault.

**Measured cost.** On ffmpeg 6.1.1, round two decoded 209 generated M4As
and 78 of 83 public sample files from real encoders (afconvert, fdkaac,
Nero, FAAC, QuickTime, ALAC 24 bit and 6 channel) with nothing said; the 5
refused also exit non zero. Static builds of other versions could not be
fetched here. The Mac's ffmpeg is read by the attended check this unit
files.

**Closes when:** the attended check counts no library M4A refused that
plays, on the Mac's ffmpeg. Ledger only.
