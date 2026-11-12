---
title: A librosa release U264 did not measure mixes to mono at the old speed, silently
found: at the build of #693, U264, 2026-11-12.
issue: no
---

**The mechanism.** `decode.mono` takes the one add only on a release named
in `decode._MEASURED_MIX` (0.10.2, 0.10.2.post1, 0.11.0, 1.0.0), the
conservative call, since a later release may change `to_mono` as 1.0 did.
Any other release, a 1.0.1 included, mixes through `librosa.to_mono`, the
same samples at the old cost, and nothing says so: no doctor row, no line in
the run's timings.

**Measured cost.** About a quarter of a second a decode on a 345 second
stereo track (812 against 501 ms at 22,050 Hz on 1.0.0, measured here), so
about half a second a track scored for vocals, once the installed librosa
moves past the table. No sample changes.

**Closes when:** a release is measured and named in the table when the
lock or an install moves to it (the librosa half of the decode tests checks
the installed release against its own `to_mono`), or the timings name the
mix that ran. Ledger only.
