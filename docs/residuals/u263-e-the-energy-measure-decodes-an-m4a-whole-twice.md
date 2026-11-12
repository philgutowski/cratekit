---
title: The energy measure of restamp and calibrate decodes an M4A whole twice, once for its length and once for its slice
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** `energy.features_from_path` asks `decode.duration` and
then `decode.load` with an offset and a duration. For a file libsndfile
reads both are a header read and a seek; for an M4A through ffmpeg each is a
whole decode, cut afterwards. The docstring says so.

**Measured cost.** Counted by the review on a 200 second ALAC: two ffmpeg
runs of 70,560,068 bytes each in one measure. No timing was taken; speed is
out of the card's scope.

**Closes when:** the ffmpeg path decodes once per measure, or asks ffmpeg
for the slice. Ledger only.
