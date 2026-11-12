---
title: A damaged but playable MP3 or FLAC is analysed on an older librosa and skipped-undecodable on librosa 1.0
found: at the review of #692, U263, round one, 2026-11-12.
issue: no
---

**The mechanism.** libsndfile opens the file and fails part way through
it. An older librosa then reads it through audioread; 1.0 has no fallback
and raises. `decode.load` keeps that failure as the caller's on purpose,
since a file libsndfile opens is never handed to ffmpeg, so the librosa
version decides whether such a file is analysed, on the base and the branch
alike.

**Measured cost.** Driven by the review with 2000 bytes zeroed in an MP3
and a FLAC: a head on 0.10.2.post1, `skipped-undecodable` on 1.0.0. Hand
damaged files; no producer was driven.

**Closes when:** decided which answer is right for a damaged file and both
librosa versions give it. Ledger only.
