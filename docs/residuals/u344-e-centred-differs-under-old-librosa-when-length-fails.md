---
title: under a librosa before 1.0, decode.centred reads ffmpeg's samples where the old composition read audioread's, when the length read fails
found: at round two of the review of #996, U344, 2026-11-23.
issue: no
---

**The mechanism.** `decode.centred` replaced the energy measure's two calls
(a length, then a windowed load). When `librosa.get_duration` fails for a
file libsndfile does not open, `centred` decodes it through ffmpeg; the old
composition's load went through `librosa.load`, which under a librosa
before 1.0 reads the file through audioread. The review forced
`get_duration` to raise under librosa 0.10.2.post1 and found 3 of 4 M4As
measured from different samples. Untouched, 15 of 15 files were identical,
and so were 165 comparisons on librosa 1.0.1. No real file was found that
takes that path.

**Cost today.** None produced: the shipped stack is librosa 1.0, and the
path needs a length read that fails on a file audioread can decode.

**Closes when:** a real file is found that takes the path, or `centred`
under a librosa before 1.0 falls back as `load` does. Ledger only.
