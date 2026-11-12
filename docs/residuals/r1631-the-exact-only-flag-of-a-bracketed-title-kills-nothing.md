---
title: The exact only flag of a title of brackets alone kills nothing in the title matcher
found: at the review of #770, R-1631, round one, 2026-11-12.
issue: no
---

**The mechanism.** `_title_core` marks a title of bracket groups alone,
"(Intro)", as compared exactly, and `_readings` then gives it no shed
reading. With the flag forced false the three matcher test files pass 624 of
624: the only pairs it changes are of the shape "(Love) (Is)" against "Love
Is", which no table holds.

**Measured cost.** None to a person: a maintainer facing guard no test pins.

**Closes when:** a test drives a pair the flag decides, or the flag is
removed. Ledger only.
