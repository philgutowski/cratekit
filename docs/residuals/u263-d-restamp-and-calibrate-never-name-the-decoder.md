---
title: analyze restamp and analyze calibrate count an M4A without ffmpeg as features-unavailable and never name the decoder
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** `energy.features_from_path` returns None for every
failure, `DecoderMissing` included, as the plan chose, so the energy measure
of restamp and calibrate cannot tell a missing decoder from a file it could
not measure.

**Measured cost.** Driven by the review with ffmpeg off the PATH over 12
M4As: restamp settled 12 of 12 `features-unavailable`, outcome ok; calibrate
reported 0 of 12 measurable with the remedy "check the command line". With
ffmpeg present both worked. The guide says what each reports.

**Closes when:** the energy measure carries the decoder's absence up as its
own reason, and calibrate's refusal names ffmpeg. Ledger only.
