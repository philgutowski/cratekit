---
title: Test slice four is 7.95 percent smaller, short of its 59,053 line bar and of the 13.97 percent share
found: at the build of #984, U335, 2026-11-24.
issue: no
---

**The mechanism.** The brief fixed the slice at 95 files and 68,640 lines on `d289f61` and its bar at 59,053. By the card's start eleven new test files had landed inside the same path range (U339, U340, R-1716, R-1950, R-1991, R-2020) and the old files had grown, so the range held 106 files and 74,245 lines. Eight builders trimmed it to U312's rules, folds through parametrize, shared helpers and builders, prose cut to the rule and its reason, with no blank line removed inside a test body and no statement packed, and reached 68,342: 5,903 fewer, 7.95 percent (per run of files 3.2, 4.9, 11.0, 9.0, 9.0, 9.3, 7.0 and 10.2 percent). Each stopped for the reason R-1941 gave: docstrings were already one line (3,276 docstring and 1,611 comment lines of 74,245), and the tests are distinct scenarios whose setup differs, so a fold needs a branch per row, and every helper pays its own def, docstring and two blank lines.

**Measured cost.** The slice is 9,289 lines over the brief's bar and 4,469 over the share floor of 63,873. No person using a verb pays for it; the epic's point 5 line bar stays missed by this slice's share.

**Closes when:** the audit card of U290 (#987, U338) settles point 5's line bar against the suite as it now stands, by a measure that does not count the separating blank lines PEP 8 requires, or by a card that removes whole tests a stronger test covers. Ledger only: maintainer facing.
