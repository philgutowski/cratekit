---
title: analyze run decodes an M4A whole twice, once for the head and once for the energy slice, 1.3 seconds a track more than before U344
found: at the build of #996, U344, 2026-11-23.
issue: no
---

**The mechanism.** Since U344 the head measures energy through the
restamp's own measure, `energy.features_from_path`, so the slice is decoded
on its own after the head's whole decode. For a file libsndfile opens that
is a seek and a two minute read. A file only ffmpeg reads, an M4A on
librosa 1.0, has no seek: the measure decodes it whole once more (once,
since U344 closed R-1556's second decode) and cuts the slice from it.

**Measured cost.** One reading each on the cloud container, the 16 M4A
transcodes of the fixed set in `scripts/analyze_stages.py`: the head's
energy stage 28.2 s before, 48.7 s after, so `analyze run` by hand takes
about 1.3 s a track more on an M4A. A tail pass over the same files is
faster, 49.4 s in all, since the restamp no longer measures them, and a
hand `analyze restamp` over them went from 69.9 s to 52.5 s.

**Closes when:** the head hands the energy measure the native samples it
already decoded for a file only ffmpeg reads, cut and resampled as the
restamp cuts them, within the light worker's declared memory. Ledger only.
