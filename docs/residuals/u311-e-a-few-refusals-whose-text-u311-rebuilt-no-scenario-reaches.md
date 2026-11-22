---
title: A few mastering and set builder refusals whose text U311 rebuilt from the same words are reached by no behaviour scenario
found: at the review of #868, U311, 2026-11-22.
issue: no
---

**The mechanism.** U311 rebuilt some refusal messages and steps in
`src/cratekit/modules/tools/mastering.py`, `src/cratekit/master/cli.py` and
`src/cratekit/setbuilder/cli.py` from shared pieces (the two not indexed
messages share one suffix, the output exists sentence is one function).
Review drove each base against branch and found them byte identical, and
U311 added scenarios for `--lufs` out of range, ffprobe missing, and `--key`
or `--bpm` beside an owned anchor. Still reached by no scenario: a split
recording refused for its layout or a missing part, an anchor inside an
excluded folder, and an absent library root. Mutating the not indexed wording
or the `--lufs` step survives the unit suite on the base as well.

**Measured cost.** None today: every one is byte identical, driven. A later
change to that wording would pass the behaviour comparison.

**Closes when:** `tests/behaviour/master.py` and `setbuilder.py` drive the
three cases, or the unit suites pin their text. Ledger only.
