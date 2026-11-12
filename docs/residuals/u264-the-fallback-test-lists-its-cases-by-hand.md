---
title: U264's fallback test says anything but two float32 channels and lists seven cases by hand
found: at the review of #693, U264, 2026-11-12.
issue: no
---

**The mechanism.** `test_anything_but_two_float32_channels_is_to_monos` in
`tests/test_analysis_decode_librosa.py` names a whole class and drives seven
members of it: mono, three channels, float64, one row, float16, big endian
and three dimensional. A value that is not an ndarray is not among them.

**Measured cost.** None. The two producers, `librosa.load` and
`decode._ffmpeg_samples`, were driven and hand `decode.mono` only native
float32 ndarrays; the review drove a big endian buffer through the mix and
found it equal to `to_mono`.

**Closes when:** the test's name says what it drives, or a property test
draws the shapes and dtypes. Ledger only.
