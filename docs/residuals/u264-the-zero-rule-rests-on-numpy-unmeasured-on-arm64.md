---
title: The mono mix's zero rule rests on numpy's add reduction starting from plus zero, unmeasured on arm64 macOS
found: at the review of #693, U264, 2026-11-12.
issue: no
---

**The mechanism.** `decode._MEASURED_MIX` holds, per librosa release, the
sign a zero takes in `librosa.to_mono`. Part of that rule is numpy's: its
add reduction starts from its identity, plus zero, so two minus zero
channels mean to plus zero, and the one add reproduces that with `+= 0`. The
table is keyed on the librosa release alone. The review measured the rule
the same on numpy 1.26.0, 1.26.4, 2.0.2, 2.1.3, 2.2.6, 2.3.5, 2.4.1 and
2.5.4, on Linux x86_64 only.

**Measured cost.** None measured. A numpy that started a float reduction
from its first element, or a build on arm64 that did, would differ from
librosa only in the sign of a zero sample of a frame whose two channels are
both minus zero, and `test_the_mix_is_the_installed_librosas_to_mono_bit_for_bit`
fails wherever the suite runs with the analysis extra, so the Mac battery
reads it.

**Closes when:** the macOS battery with the analysis extra passes the
librosa half of the decode tests on the Mac's numpy. Ledger only.
