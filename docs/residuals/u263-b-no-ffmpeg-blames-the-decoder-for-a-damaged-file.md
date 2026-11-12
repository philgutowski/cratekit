---
title: Without ffmpeg a damaged file libsndfile cannot open settles skipped-no-decoder rather than skipped-undecodable
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** `decode.load` cannot tell an M4A from a file too damaged
for libsndfile to open without trying ffmpeg, so with ffmpeg absent both
raise `DecoderMissing`, which the head reports as `skipped-no-decoder`. The
docstrings and the guide now say so.

**Measured cost.** Driven by the review with ffmpeg off the PATH: an empty
FLAC, a headless FLAC and random bytes named MP3 settled
`skipped-no-decoder`, where the base said `skipped-undecodable`. Nothing is
written or lost; doctor already fails `binary.ffmpeg` on such a machine, and
a rerun with ffmpeg present settles each file correctly.

**Closes when:** the status says "no decoder tried" in words a person reads
that way, or the head tells an M4A by its container header before blaming
the decoder. Ledger only.
