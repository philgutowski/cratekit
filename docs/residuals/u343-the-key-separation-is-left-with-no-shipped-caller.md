---
title: analysis/separation.py's harmonic function has no shipped caller since the run stopped reading a key
found: at the build of #995, U343, 2026-11-23.
issue: no
---

**The mechanism.** `separation.harmonic` separated the harmonic part the key's
chroma was read from under the `whole` and `windows` key methods. U343 took
the key out of the run, so nothing under `src` calls it; only
`tests/test_analysis_separation.py` does. `separation.harmonic_percussive`,
which the energy measure calls, shares its module and stays used. Left in
place because the brief named the detector, the agreement and the check, not
the separation module, and its pins guard the energy's sibling.

**Measured cost.** None to a person: a function and its tests a maintainer
reads and keeps green for nothing. Its five tests that fail under librosa
1.0.1 on main and the branch alike are R-1633's, not this one.

**Closes when:** `separation.harmonic` and its tests are removed, or a later
unit names a caller for it. Ledger only, maintainer facing.
