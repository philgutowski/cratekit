---
title: On librosa 1.0.1 the separation's percussive half is not librosa's element for element, a last place apart, and the five tests that say so fail on main
found: at the build of #731, U276, 2026-11-12.
issue: no
---

**The mechanism.** `tests/test_analysis_separation.py::test_the_harmonic_and_percussive_pair_is_librosas_element_for_element`
holds `separation.harmonic_percussive` equal to `librosa.effects.hpss` with
`array_equal`. Under librosa 1.0.1 and numpy 2.5.4, installed fresh with the
analysis extra on a Linux container, the harmonic half is equal and the
percussive half is not: at every one of the five lengths (7680, 8000, 22050,
154363, 1345050 samples) a few elements differ in the last place, for example
`-0.05020787` against `-0.05020786`. The same five fail on `main` at
`bf89ec0c`, so the cause is the installed release, not U276: on the same
container with librosa 1.0.0 and the same numpy, all fifty of the module's
tests pass. U241 and U264 measured the separation on 1.0.0 and 0.10.2.post1.
The key no longer reads the separation by default (U276); the energy pass
still reads the percussive half.

**Measured cost.** Not driven to a user facing cost. A last place difference
in the percussive half moves an energy feature by far less than a level's
width, so no energy level was seen to change; the cost is that the module's
claim of librosa's arithmetic bit for bit is false on 1.0.1, and
that five tests fail on any machine that installs it, which the Mac's
battery will show if it has.

**Closes when:** the cause on 1.0.1 is found (most likely a changed order of
operations in librosa's own `hpss` mask, `softmask`, or its `istft`), and the
separation matches it on that release the way U264 gave the mix a table per
release, or the test states the release it holds for. Ledger only:
maintainer facing, no person using the verbs pays for it.
