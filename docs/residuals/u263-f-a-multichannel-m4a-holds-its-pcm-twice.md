---
title: A multichannel M4A decoded through ffmpeg holds its native samples twice, above the light worker's declared cost
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** `decode._ffmpeg_samples` reads ffmpeg's whole output into
one bytes object and views it as float32, and the mix to mono then builds
its own array, while a libsndfile read is planned at one native copy. The
light worker's declared cost (U241) is per second of track, not per channel.

**Measured cost.** Single readings by the review, 400 second files: a 5.1
ALAC peaked at 883 MB against 622 MB for the same audio as FLAC and a
planned 606 MB; stereo peaked at 353 MB either way, inside the plan. No
producer of a multichannel M4A in the library was driven.

**Closes when:** the ffmpeg path streams its output, or asks ffmpeg for the
mono mix, or the worker's cost counts channels. Ledger only.
