---
title: The Cyanite trial sends MP3s only, so a filed track held as AIFF, WAV or FLAC cannot be measured
found: at the build of #674, U245, 2026-11-13.
issue: no
---

**The mechanism.** Cyanite's API takes MP3 uploads of up to fifteen minutes,
by its documentation, so `tagging/cyanite.py` sends a file only when its
suffix is `.mp3` and lists every other file as not sent. Nothing converts a
lossless file for the trial. A file over fifteen minutes is uploaded and its
refusal, whatever Cyanite answers, is written on its row.

**Measured cost.** A trial over folders of lossless files measures nothing
for them, and says so on each one. How much of the filed library is MP3 is
unmeasured. Converting was out of the card's scope; whether the trial should
convert a temporary copy is asked on the card as a Question for Phillip.

**Closes when:** Phillip chooses MP3s for the trial, or a later card converts
a temporary MP3 copy of each chosen lossless file for the upload and deletes
it after. Ledger only.
