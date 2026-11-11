---
title: U212's branches for a pass landing what is staged are reached by nothing
found: at the review of #665, R-1499, round one, 2026-11-11.
issue: no
---

**The mechanism.** Since R-1499 a pass whose missing tracks are staged by another download refuses before its download, so `_download`'s `listed.path is None` branch, `_staged_on` and the "downloaded nothing ... over what is staged" sentence in `_attended` in `cli/sync_land.py` are reached only when the staged tracks are the pass's own, which the listing excludes.

**Measured cost.** Replacing each with a raise killed nothing over ten test files (round one, mutation rows N1 to N3); one candidate for reaching them was driven (d9) and does not. No user facing cost; text nobody sees.

**Closes when:** the branches are removed, or a test reaches them. Ledger only.
