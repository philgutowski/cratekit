---
title: The dependency allows any rapidfuzz from 3.0, and the width dependent whitespace the sorted word pass copies was measured on 3.14 only
found: at the review of #694, U265, 2026-11-12.
issue: no
---

**The mechanism.** `pyproject.toml` asks for `rapidfuzz>=3.0`. U265's `_sorted_words` copies the compiled scorer's word split, which differs by string width, and that split was measured over every code point on 3.14.6, the version this tree installs. An older or newer release that splits differently, and above all one that did not split on U+001F, which joins every recording token, would move approximate answers.

**Measured cost.** Unmeasured: no other version was installed and none was downloaded. U265's whitespace and whole matrix tests would fail on such an install, so a difference would be loud in the suite rather than silent in a run.

**Closes when:** the floor is raised to the measured release, or the split is measured on the floor release too. Ledger only.
